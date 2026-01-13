import rclpy
import time
from rclpy.node import Node
import cflib.crtp
from cflib.crazyflie import Crazyflie, Extpos
from cflib.positioning.position_hl_commander import PositionHlCommander
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from motion_capture_tracking_interfaces.msg import NamedPoseArray, NamedPose
from geometry_msgs.msg import Point
from std_srvs.srv import Trigger
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from rclpy.qos import ReliabilityPolicy, QoSProfile
from rclpy.duration import Duration
from cflib.utils.reset_estimator import reset_estimator
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from geometry_msgs.msg import PoseStamped
from threading import Thread
#from cflib.crazyflie.swarm import CachedCfFactory
#from cflib.crazyflie.swarm import Swarm            <- !!!

from geometry_msgs.msg import Pose




class CrazyflieControl(Node):
    

    def __init__(self ):
        super().__init__('crazyflie_control')
        self.crazyflie = None
        self.declare_parameter('cf_name', 'crazyflie_5')
        self.declare_parameter('link_uri', "radio://0/5/2M/E7E7E7E705")
        self.cf_name = self.get_parameter('cf_name').value
        self.link_uri = uri_helper.uri_from_env(
            default=self.get_parameter('link_uri').value)
        
        
        
        self.get_logger().info('crazyflie name: "%s"' % self.cf_name)
        self.get_logger().info('link uri: "%s"' % self.link_uri)
        
        # plusieurs callback du même groupe peuvent êre créer en parallèle
        self.clb_group = ReentrantCallbackGroup()
        self.init_cf_pose = False
        self.is_takeoff = False  # état du drone (a t-il décollé ?)
        self.is_init = False
        self.target_pose = PoseStamped().pose

        
        # Topic pour les positions avec mocap_node
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.sub_get_pose = self.create_subscription(PoseStamped, f"/{self.cf_name}/pose", self.clb_poses, qos, callback_group=self.clb_group )
        self.service_takeoff = self.create_service(Trigger, f"/{self.cf_name}/takeoff", self.takeoff,  callback_group=self.clb_group)
        self.service_land = self.create_service(Trigger, f"/{self.cf_name}/land", self.clb_land,  callback_group=self.clb_group)
        self.set_point = self.create_subscription(PoseStamped, f"/{self.cf_name}/TargetPose", self.sub_sendposition_setpoint, 10)
        self.timer_setpoint = self.create_timer(0.1, self.timer_clb_positions, callback_group=self.clb_group)
        

        # envoie les positions mocap au drone

    def clb_poses(self, msg):
        #self.get_logger().info('crazyflie name: "%s"' % self.cf_name)
        if not self.init_cf_pose:
            self.target_pose = msg.pose
            self.init_cf_pose = True
        if self.crazyflie:
            self.crazyflie.extpos.send_extpos(msg.pose.position.x,
                                              msg.pose.position.y, 
                                              msg.pose.position.z)

    def sub_sendposition_setpoint(self, msg):
        if self.is_takeoff:
            if float(msg.pose.position.z) < 0.1:
                msg.pose.position.z = str(self.target_pose.position.z)
            self.target_pose = msg.pose

    # envoie les positions cibles au drone
    def set_position(self, pose):
        x = float(pose.position.x)
        y = float(pose.position.y)
        z = float(pose.position.z)
        yaw = float(pose.orientation.z)
        if self.crazyflie:
            self.crazyflie.commander.send_position_setpoint(x, y, z, yaw)

    def timer_clb_positions(self):

        
        if self.is_takeoff:
            self.set_position(self.target_pose)

    def setup_parameters(self):
        """
        Configure le Crazyflie pour le vol en mode position externe (Mocap).
        """
        assert self.crazyflie, f"{self.cf_name} n'est pas connecté" 
        print("Configuration des paramètres...")

        self.crazyflie.param.set_value('stabilizer.estimator', '2')
        #self.crazyflie.param.set_value('locSrv.extPosStdDev', 0.001)
        #self.crazyflie.param.set_value('locSrv.extQuatStdDev', 0.05)
        self.crazyflie.param.set_value('stabilizer.controller', '1')
        time.sleep(0.1)

        # Réinitialiser le filtre Kalman
        reset_estimator(self.crazyflie)
        time.sleep(0.1)

    def takeoff(self, request, response):
        if not self.is_init:
            self.setup_parameters()
            self.is_init = True
   
        
        self.target_pose.position.z = 1.0
        for _ in range(20):
            self.set_position(self.target_pose)
            time.sleep(0.1)
        self.is_takeoff = True
        response.success = True
        return response

    # callback land appelé par le service
    def clb_land(self, request, response):
        self.land()
        response.success = True
        return response

    def land(self):
        self.is_takeoff = False
        # if not self.is_takeof:
        # self.crazyflie.high_level_commander.land(0.0, 2.0)
        self.target_pose.position.z = 0.1
        for _ in range(20):
            self.set_position(self.target_pose)
            time.sleep(0.1)

        self.crazyflie.commander.send_stop_setpoint()
        # Hand control over to the high level commander to avoid timeout and locking of the Crazyflie
        self.crazyflie.commander.send_notify_setpoint_stop()


def main(args=None):
    
    rclpy.init(args=args)
    
    
    cflib.crtp.init_drivers()
    node = CrazyflieControl()  # Création du nœud
    uri = node.link_uri
    
    
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf: #with Swarm(link_uris, factory=factory) as swarm:
    #scf =  SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) 
        
        #factory = CachedCfFactory(rw_cache='./cache')
        node.crazyflie = scf.cf #remplacer scf par swarm
        node.get_logger().info(f"uri: {uri} | name: {node.cf_name}")
        
        
        executor = MultiThreadedExecutor()
        executor.add_node(node)
        executor.spin()
        # node.crazyflie.commander.send_velocity_world_setpoint(0,0,0,0)
        node.land()

        
        # node.crazyflie.close_link() #initie la connexion au drone
        time.sleep(2.0)
        
        # node.crazyflie.disconnected()
        node.destroy_node()  # Destruction du nœud lors de l'arrêt
        rclpy.shutdown()  # Arrêt de ROS


if __name__ == '__main__':
    main()
