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
from rclpy.duration import Duration
from cflib.utils.reset_estimator import reset_estimator
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from geometry_msgs.msg import PoseStamped
from threading import Thread
from geometry_msgs.msg import Pose
import motioncapture

host_name = '192.168.2.10'

# The type of the mocap system
# Valid options are: 'vicon', 'optitrack', 'optitrack_closed_source', 'qualisys', 'nokov', 'vrpn', 'motionanalysis'
mocap_system_type = 'optitrack'

# The name of the rigid body that represents the Crazyflie
rigid_body_name = 'crazyflie_1' #mettre de nom de l'objet rigid qui est dans optitrack

# True: send position and orientation; False: send position only
send_full_pose = False

                        

def send_extpose_quat(cf, x, y, z, quat):
    """
    Send the current Crazyflie X, Y, Z position and attitude as a quaternion.
    This is going to be forwarded to the Crazyflie's position estimator.
    """
    if send_full_pose:
        cf.extpos.send_extpose(x, y, z, quat.x, quat.y, quat.z, quat.w)
    else:
        cf.extpos.send_extpos(x, y, z)

sequence = [
    (0.0, 0.0, 0.5, 0),
    (0.5, 0.0, 0.5, 0.0),
    (0.5, 0.0, 0.5, 90.0),
    (0.5, 0.5, 0.5, 90.0),
    (0.5, 0.5, 0.5, 180.0),
    (0.0, 0.5, 0.5, 180.0),
    (0.0, 0.5, 0.5, 270.0),
    (0.0, 0.0, 0.5, 270.0),
    (0.0, 0.0, 0.5, 0.0),
    (0.0, 0.0, 0.15, 0.0),
    #(-0.5, 0.5, 1.2, 0),
    #(-0.5, -0.5, 1.2, 0),
    #(0.0, 0.0, 1.2, 0),
    #(0.0, 0.0, 0.4, 0),
    #(0.0, 0.0, 0.0, 0),
]
 
class MocapWrapper(Thread):
    def __init__(self, body_name):
        Thread.__init__(self)

        self.body_name = body_name
        self.on_pose = None
        self._stay_open = True

        self.start()

    def close(self):
        self._stay_open = False

    def run(self):
        mc = motioncapture.connect(mocap_system_type, {'hostname': host_name})
        while self._stay_open:
            mc.waitForNextFrame()
            for name, obj in mc.rigidBodies.items():
                if name == self.body_name:
                    if self.on_pose:
                        pos = obj.position
                        self.on_pose([pos[0], pos[1], pos[2], obj.rotation])

class CrazyflieControl(Node):
    mocap_wrapper = MocapWrapper(rigid_body_name)
    def __init__(self, cf):
        super().__init__('crazyflie_control')  # Nom du nœud
        self.cf_name = "crazyflie_1" #Nom du crazyflie
        self.clb_group = ReentrantCallbackGroup() #plusieurs callback du même groupe peuvent êre créer en parallèle
        
        self.is_takeof = False #état du drone (a t-il décollé ?)
        self.is_set_parameters = False
        self.cmp = 0
        self.sequence_index = 0
        self.connected = False
        self.pose = PoseStamped().pose
        self.free = True
        

        # Initialiser les CrazyRadios pour se connecter le drone
        #cflib.crtp.init_drivers()
        #available = cflib.crtp.scan_interfaces()
        #self.link_uri = "" #permet de stocker l'addresse
        #for i in available:
        #    radio_name = i[0]
        #    print("Interface with URI [%s] found and name/comment [%s]" % (radio_name, i[1]))
        #    if "radio" in radio_name:
        #        self.link_uri = radio_name
            

        self.link_uri = uri_helper.uri_from_env(default='radio://0/5/2M/E7E7E7E7E7') #entrer la radio de l'optitrack
        #self.syncrazyflie = SyncCrazyflie(uri, cf = Crazyflie(rw_cache='./cache')) #création d'un objet python représentant le drone)
        #self.syncrazyflie.open_link()
        #print(uri)
        self.crazyflie = cf #Crazyflie(rw_cache='./cache')

        
        #évènement : quand la connection au drone est établie
        #self.crazyflie.connected.add_callback(self.crazyflie_connected)
        #time.sleep(2.0)
        #self.crazyflie.open_link(self.link_uri) #initie la connexion au drone en précisant l'addresse
        #time.sleep(2.0)
        #if self.syncrazyflie.is_link_open(): 
        # envois des commandes une fois la connexion établie
        
    

        #Topic pour les positions avec mocap_node
        
        self.service_takeoff = self.create_service(Trigger, '/takeoff',self.takeoff,  callback_group=self.clb_group)
        self.service_land = self.create_service(Trigger, '/land',self.clb_land ,  callback_group=self.clb_group)
        self.set_point = self.create_subscription(PoseStamped, '/TargetPose', self.sub_sendposition_setpoint, 10)
        self.timer_setpoint = self.create_timer(0.1, self.timer_clb_positions)
        self.sub_position = self.create_subscription(Pose, '/crazyflie_1/pose', self.clb_poses, 10, callback_group=self.clb_group)

        #envoie les positions mocap au drone
    def clb_poses(self,msg_poses) :
        cf_pose = msg_poses.position
        #print(float(cf_pose.x), float(cf_pose.y), float(cf_pose.z))
        self.crazyflie.extpos.send_extpos(float(cf_pose.x), float(cf_pose.y), float(cf_pose.z)) 
            

    def sub_sendposition_setpoint(self, msg):

        if self.is_takeof:
            if float(msg.pose.position.z) < 0.1:
                msg.pose.position.z = str(self.pose.position.z)
            self.pose = msg.pose
            
    #envoie les positions cibles au drone
    def set_position(self, pose):
        x   = float(pose.position.x)
        y   = float(pose.position.y)
        z   = float(pose.position.z)
        yaw = float(pose.orientation.z)
    
        self.crazyflie.commander.send_position_setpoint(x, y, z, yaw)


    def timer_clb_positions(self):
        #if not self.is_set_parameters:
        #    self.setup_parameters(self.crazyflie) 
        #    self.is_set_parameters = True
        if self.is_takeof:
            self.set_position(self.pose)


    def setup_parameters(self, cf):
        """
        Configure le Crazyflie pour le vol en mode position externe (Mocap).
        """
        print("Configuration des paramètres...")
        self.free=False

        cf.param.set_value('stabilizer.estimator', '2')
        cf.param.set_value('locSrv.extPosStdDev', 0.001)
        cf.param.set_value('locSrv.extQuatStdDev', 0.05)
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(2.0)

        # Réinitialiser le filtre Kalman
        reset_estimator(cf)
        time.sleep(2.0)
        self.free=True

    #appelé lorsque la connexion au drone est établie
    def crazyflie_connected(self, uri):
        print("Connecté au drone :", uri)
        self.connected = True

              
           
    def takeoff(self, request, response): 
        #if not self.is_takeof:
        #self.crazyflie.high_level_commander.takeoff(1.0, 2.0)
        self.pose.position.z = 1.0
        for _ in range(20):
            self.set_position(self.pose)
            time.sleep(0.1)
        self.is_takeof = True
        response.success = True
        return response
    
    #callback land appelé par le service
    def clb_land(self, request, response):
        self.land()        
        response.success = True
        return response

    def land(self):
        self.is_takeof = False
        #if not self.is_takeof:
        #self.crazyflie.high_level_commander.land(0.0, 2.0)
        self.pose.position.z = 0.1
        for _ in range(20):
            self.set_position(self.pose)
            time.sleep(0.1)
        
        self.crazyflie.commander.send_stop_setpoint()
        # Hand control over to the high level commander to avoid timeout and locking of the Crazyflie
        self.crazyflie.commander.send_notify_setpoint_stop()

def activate_kalman_estimator(cf):
    cf.param.set_value('stabilizer.estimator', '2')

    # Set the std deviation for the quaternion data pushed into the
    # kalman filter. The default value seems to be a bit too low.
    cf.param.set_value('locSrv.extQuatStdDev', 0.06)


def activate_mellinger_controller(cf):
    cf.param.set_value('stabilizer.controller', '2')

def main(args=None):
    cflib.crtp.init_drivers()
    uri = uri_helper.uri_from_env(default='radio://0/5/2M/E7E7E7E7E7')
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf
        rclpy.init(args=args)
        executor = MultiThreadedExecutor()
        node = CrazyflieControl(cf)  # Création du nœud
        node.mocap_wrapper.on_pose = lambda pose: send_extpose_quat(cf, pose[0], pose[1], pose[2], pose[3])
        activate_kalman_estimator(cf)
        reset_estimator(cf)
        executor.add_node(node)

        #rclpy.spin(node)  # Exécution du nœud

        executor.spin()
        #node.crazyflie.commander.send_velocity_world_setpoint(0,0,0,0)
        node.land()

        #time.sleep(2.0)

        #node.crazyflie.close_link() #initie la connexion au drone
        time.sleep(2.0)
        #node.crazyflie.disconnected()
        node.destroy_node()  # Destruction du nœud lors de l'arrêt
        rclpy.shutdown()  # Arrêt de ROS

if __name__ == '__main__':
    main()