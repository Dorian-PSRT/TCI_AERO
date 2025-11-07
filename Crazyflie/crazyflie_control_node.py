import rclpy
import time
from rclpy.node import Node 
import cflib.crtp
from cflib.crazyflie import Crazyflie, Extpos
from cflib.positioning.position_hl_commander import PositionHlCommander
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from motion_capture_tracking_interfaces.msg import NamedPoseArray, NamedPose
from geometry_msgs.msg import Point
from std_srvs.srv import Trigger 
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from rclpy.duration import Duration

class CrazyflieControl(Node):
    def __init__(self):
        super().__init__('crazyflie_control')  # Nom du nœud
        self.cf_name = "crazyflie_1" #Nom du crazyflie
        self.clb_group = ReentrantCallbackGroup() #plusieurs callback du même groupe peuvent êre créer en parallèle
        self.is_takeof = False #état du drone (a t-il décollé ?)
        

        # Initialiser les CrazyRadios pour se connecter le drone
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()
        self.link_uri = "" #permet de stocker l'addresse
        for i in available:
            radio_name = i[0]
            print("Interface with URI [%s] found and name/comment [%s]" % (radio_name, i[1]))
            if "radio" in radio_name:
                self.link_uri = radio_name
            

        self.crazyflie = Crazyflie() #création d'un objet python représentant le drone
        #évènement : quand la connection au drone est établie
        self.crazyflie.connected.add_callback(self.crazyflie_connected)

        self.crazyflie.open_link(self.link_uri) #initie la connexion au drone en préceisant l'addresse

        self.setup_parameters(self.crazyflie)
        #Création d'un conttrôleur de position
        self.PHC = PositionHlCommander(self.crazyflie) #cette classe permet de commander le drone par position

        qos_profile = QoSProfile(reliability =QoSReliabilityPolicy.BEST_EFFORT,
                history=QoSHistoryPolicy.KEEP_LAST,
                depth=1,
                deadline = Duration(seconds=0, nanoseconds=1e9/100.0))

        self.sub_cf_pose = self.create_subscription(NamedPoseArray, "/poses", self.clb_poses,10)
        self.service = self.create_service(Trigger, '/takeoff',self.takeoff, callback_group=self.clb_group)

        
    def setup_parameters(self, cf):
        """
        Configure le Crazyflie pour le vol en mode position externe (Mocap).
        """
        print("Configuration des paramètres...")
        #Active le mode de commande de haut niveau (High-Level Commander)
        cf.param.set_value('commander.enHighLevel', '0')
        cf.param.set_value('flightmode.posSet', '1')
        cf.param.set_value('flightmode.stabModeRoll', '0')
        cf.param.set_value('flightmode.stabModePitch', '0')
        cf.param.set_value('flightmode.stabModeYaw', '0')

        # Réinitialiser le filtre Kalman
        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')

        # Vérification de la configuration
        en_hlc = cf.param.get_value('commander.enHighLevel')
        print(f"  commander.enHighLevel = {en_hlc}")
        

    #appelé lorsque la connexion au drone est établie
    def crazyflie_connected(self, uri):
        print("Connecté au drone :", uri)
        time.sleep(1)
        # envois des commandes une fois la connexion établie
        #self.send_setpoint()

    def clb_poses(self,msg_poses) :
        for msg_pose in msg_poses.poses:
            if msg_pose.name == self.cf_name:
                cf_pose = msg_pose.pose.position
                
                #print(f"{msg_pose.name} - {cf_pose}")

                self.crazyflie.extpos.send_extpos(cf_pose.x, cf_pose.y, cf_pose.z)
                
                
                if True: #abs(cf_pose.x) <= 1.0 and abs(cf_pose.y) <= 1.0 and abs(cf_pose.z) <= 2.0:
                    
                    #self.crazyflie.commander.send_velocity_world_setpoint(1.0 * (0.0-cf_pose.x), 1.0 * (0.0-cf_pose.y), 0.5 * (1.0-cf_pose.z) ,0)
                    uz = 0.5 * (1.0-cf_pose.z)
                    uz = min(max(uz, -1), 1)
                    thrust = (60_000-10_001)/2.0 *uz + (60_000+10_001)/2.0

                    thrust = int(min(max(thrust, 0), 60000))
                    print(f"{thrust}")
                    self.crazyflie.commander.send_setpoint(0.0 * (0.0-cf_pose.x), 0.0 * (0.0-cf_pose.y), 0.0, thrust)
                else:
                    self.crazyflie.commander.send_setpoint(0.0,0.0,0.0,0.0)
                    #self.crazyflie.commander.send_velocity_world_setpoint(0,0,0,0)
        #if cf_pose.z > 1.0:
        #    self.crazyflie.commander.send_velocity_world_setpoint(0,0,0,0)

            
    def takeoff(self, request, response):
        #if not self.is_takeof:
        self.PHC.take_off(1.0)
        self.is_takeof = True
        response.success = True
        return response

def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()
    node = CrazyflieControl()  # Création du nœud
    executor.add_node(node)
    #rclpy.spin(node)  # Exécution du nœud
    executor.spin()
    #node.crazyflie.commander.send_velocity_world_setpoint(0,0,0,0)
    node.crazyflie.commander.send_setpoint(0.0,0.0,0.0,0.0)
    node.crazyflie.close_link(node.link_uri) #initie la connexion au drone
    node.crazyflie.disconnected()
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS

if __name__ == '__main__':
    main()
