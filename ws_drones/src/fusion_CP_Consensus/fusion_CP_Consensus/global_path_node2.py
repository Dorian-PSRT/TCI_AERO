#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.qos import ReliabilityPolicy, QoSProfile
#import des types qui serviront aux services
from my_custom_interfaces.srv import Position3D
from example_interfaces.srv import Trigger
from turtlesim.srv import TeleportAbsolute
#import des types qui serviront aux topics
from std_msgs.msg import Bool
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseStamped
#import de bibliotheques pour des besoins spécifiques
from time import sleep
import json
from pathlib import Path




# Utils.json pournombre de drones
dossier = Path(__file__).parent
dossier = dossier.parents[5]
utils = dossier/"src"/"fusion_CP_Consensus"/"utils.json" 
with open(utils) as f:
    file = json.load(f)

nb_drones=int(file["nb_drones"])
mode=int(file["mode"])

# on récupère l'id du drone
id=int(__file__[-4])


class global_path(Node):
    def __init__(self):
        super().__init__('global_path_node')

        #appel de fonctions à l'initialisation

        client_cb_group    = None
        topic_cb_group     = MutuallyExclusiveCallbackGroup()  #hyper important, ça permet d'appeler un service dans un callback ! (sinon ça casse tout)
        self.recu_pos_w    = False  #on a pas encore reçu la position de la fenêtre
        self.recu_pos_init = False

        if mode :
            self.path = [(float(id)-1.0 , 2.0,  1.0), #va devenir la target Window
                    (float(id)-1.0 , 3.0,  1.0),
                    ] #définition les objectifs à atteindre sous forme de vecteur de duos de floats
        else:
            self.path = [(2.0 , 0.0 , 1.5), #définition les objectifs à atteindre sous forme de vecteur de duos de floats
                    #(-5.0, 8.0 , 2.0), #+2.0*float(id)
                    ]
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.subscriptionW = self.create_subscription(PoseStamped,'/window/pose', self.poseW,qos)
        self.subscription_go = self.create_subscription(Bool, f'/turtle{id}/go',self.send_waypoints, 10,callback_group=topic_cb_group)
        self.subscription = self.create_subscription(Pose,f'/turtle{id}/pose', self.poseInit,qos)
        self.client_goal = self.create_client(Position3D, f'/turtle{id}/set_target_pose',callback_group=client_cb_group) #global_path_node est un client du service set_target_pose proposé par local_path_node
        self.client_result = self.create_client(Trigger, f'/turtle{id}/set_result',callback_group=client_cb_group) #global_path_node est un client du service set_result proposé par local_path_node
        self.publisher_done  = self.create_publisher(Bool, f'/leader/done', 10)
        self.__wait_services() 

        #self.subscription_go = self.create_subscription(Bool, f'/turtle{id}/go',self.send_waypoints, 10,callback_group=topic_cb_group)

        self.wps = [] #la variable globale wps représente le vecteur qui donne les objectifs à atteindre

        if mode == 0:
            self.wps = self.compute_path()

        self.get_logger().info('Le nœud est démarré !')

    def __wait_services(self): # méthode privée pour attendre que les deux serveurs de local_path_node soient accessibles, avant de continuer
        wait_goal_service   = self.client_goal.wait_for_service(timeout_sec=1.0)
        wait_result_service = self.client_result.wait_for_service(timeout_sec=1.0)
        while not wait_goal_service or not wait_result_service :
            wait_goal_service   = self.client_goal.wait_for_service(timeout_sec=1.0)
            wait_result_service = self.client_result.wait_for_service(timeout_sec=1.0)
            self.get_logger().info('Services not available, waiting...')

    def poseW (self,msg):
        if not(self.recu_pos_w):
            self.path[0]=(msg.pose.position.x,msg.pose.position.y,msg.pose.position.z)
            self.recu_pos_w=True
            if self.recu_pos_init:
                self.wps = self.compute_path() #la variable globale wps représente le vecteur qui donne les objectifs à atteindre
            self.get_logger().info('Position Window reçu!')
        else:
            pass

    def poseInit (self,msg):
        if not(self.recu_pos_init):
            if len(self.path)!=1:
                x,y,z=self.path[1]
                self.path[1]=(msg.x, y, z)
            self.recu_pos_init=True
            if self.recu_pos_w or mode==0:
                self.wps = self.compute_path() #la variable globale wps représente le vecteur qui donne les objectifs à atteindre
            self.get_logger().info('Position Init reçu!')
        else:
            pass

    def compute_path(self):
        waypoints = []
        for x,y,z in self.path:
            wp = Position3D.Request() #réécriture des duos de floats sous forme du type de la requête à envoyer 
            wp.point.x = x
            wp.point.y = y  
            wp.point.z = z 
            waypoints.append(wp) #ajout du dernier point (dans le bon type) au nouveau vecteur qui donne les objectifs à atteindre
        return waypoints

    def send_waypoints(self,msg):
        while self.wps == []:
            sleep(0.1)
        if msg.data :
            for wp in self.wps:
                self.set_goal(wp)
                self.get_result(Trigger.Request())
            done=Bool()
            done.data=True
            self.publisher_done.publish(done)  #je suis arrivé
            self.get_logger().info('Le leader est arrivé !')

    def set_goal(self, request):
        future = self.client_goal.call_async(request) #Envoie la requête contenant le prochain objectif à local_path_node, future.result deviendra True quand le serveur aura répondu ""
        rclpy.spin_until_future_complete(self, future, executor=None) #Tourne en rond car pas d'executor spécifié en attendant que future.result soit True
        return future.result()
    
    """--------------------------------------Précisions sur set_goal et get_result---------------------------------------------
    call_async(request) : Make a service request and asyncronously get the result.Return type : Future.(A future completes when the request does)
    future est un type de variable très spéciale qui aloue de l'espace vide dans la mémoire qui attend une réponse asynchrone et s'actualisera tout seul au moment venu"""
        
    def get_result(self, request):
        future = self.client_result.call_async(request) #Envoie une requête vide pour demander à local_path_node si on est bien arrivé à l'objectif précédent
        rclpy.spin_until_future_complete(self, future, executor=None) #Tourne en rond car pas d'executor spécifié en attendant que future.result soit True
        return future.result()

def main(args=None):
    rclpy.init(args=args)
    node = global_path()  # Création du nœud
    rclpy.spin(node)  # Exécution du nœud
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()
