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
from std_msgs.msg import Bool,Float32
from geometry_msgs.msg import Point
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseStamped
from my_custom_interfaces.msg import Map, Go
#import de bibliotheques pour des besoins spécifiques
from time import sleep
import json
from pathlib import Path
import numpy as np



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
        self.graph         = []
        self.formation     = False
        self.lead          = False
        self.pos_init      = None
        self.repli = False
        self.future = None

        #path du leader
        if mode :
            self.path = [(float(id)-1.0 , 2.0,  1.0), #va devenir la target Window
                    (float(id)-1.0 , 3.0,  1.0),
                    ] #définition les objectifs à atteindre sous forme de vecteur de duos de floats
        else:
            # self.path = [(2.0, 0.0 , 1.5), #définition les objectifs à atteindre sous forme de vecteur de duos de floats
            #         (3.0, 0.0 , 1.5), #+2.0*float(id)
            #         ]
            self.path = [(0.0, 4.5 , 1.5), #définition les objectifs à atteindre sous forme de vecteur de duos de floats
                    (1.0, 4.5 , 1.5), #+2.0*float(id)
                    ]
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.subscriptionW      = self.create_subscription(PoseStamped,'/window/pose', self.poseW,qos)
        self.subscription_go    = self.create_subscription(Go, f'/turtle{id}/go',self.send_waypoints, 10,callback_group=topic_cb_group)
        self.subscription       = self.create_subscription(Pose,f'/turtle{id}/pose', self.poseInit,qos,callback_group=topic_cb_group)
        self.client_goal        = self.create_client(Position3D, f'/turtle{id}/set_target_pose',callback_group=client_cb_group) #global_path_node est un client du service set_target_pose proposé par local_path_node
        self.client_result      = self.create_client(Trigger, f'/turtle{id}/set_result',callback_group=client_cb_group) #global_path_node est un client du service set_result proposé par local_path_node
        self.publisher_done     = self.create_publisher(Map, f'/leader/done', 10)
        self.subscription_done  = self.create_subscription(Map, f'/leader/done', self.update_graph, 10) #ils update leur graph
        self.publisher_ready    = self.create_publisher(Bool, f'/turtle{id}/ready', 10)
        self.subscription_repli = self.create_subscription(Go, f'/turtle{id}/repli', self.repli_update, 10)
        self.dist_init          = self.create_publisher(Float32,f'/turtle{id}/err_dist', 10)
        self.timer_err          = self.create_timer(0.2, self.maj_err, callback_group=topic_cb_group)
        self.__wait_services() 
        if mode :
            self.subscription_wp = self.create_subscription(PoseStamped, f'/crazyflie_{id}/TargetPose', self.graph_build, 10)
        else:
            self.subscription_wp = self.create_subscription(PoseStamped, f'/Crazyflie{id}/pose_d', self.graph_build, 10)

        #self.subscription_go = self.create_subscription(Bool, f'/turtle{id}/go',self.send_waypoints, 10,callback_group=topic_cb_group)

        self.wps = [] #la variable globale wps représente le vecteur qui donne les objectifs à atteindre

        # if mode == 0:
        #     self.wps = self.compute_path()

        self.get_logger().info('Le nœud est démarré !')

    def __wait_services(self): # méthode privée pour attendre que les deux serveurs de local_path_node soient accessibles, avant de continuer
        wait_goal_service   = self.client_goal.wait_for_service(timeout_sec=1.0)
        wait_result_service = self.client_result.wait_for_service(timeout_sec=1.0)
        while not wait_goal_service or not wait_result_service :
            wait_goal_service   = self.client_goal.wait_for_service(timeout_sec=1.0)
            wait_result_service = self.client_result.wait_for_service(timeout_sec=1.0)
            self.get_logger().info('Services not available, waiting...')

    def repli_update(self):
        self.repli=True
        if self.future is not None:
            self.future.cancel()

        if self.lead:
            #build graph?...
            pass
        else:
            pass

    def maj_err(self):
        while self.pos_init == None:
            sleep(0.2)
        Pose_init=np.array(self.pos_init)
        Pose=np.array((self.pose.x,self.pose.y,self.pose.theta))
        d = Float32()
        d.data = float(np.linalg.norm(Pose_init-Pose))
        self.dist_init.publish(d)

    def poseW (self,msg):
        if not(self.recu_pos_w):
            self.posWindow=(msg.pose.position.x,msg.pose.position.y -0.5 ,msg.pose.position.z)
            self.path[0]=self.posWindow
            self.posWindow=(msg.pose.position.x -1.0 ,msg.pose.position.y -0.5 ,msg.pose.position.z)
            self.path[1]=self.posWindow
            self.recu_pos_w=True
            # if self.recu_pos_init:
            #     self.wps = self.compute_path() #la variable globale wps représente le vecteur qui donne les objectifs à atteindre
            self.get_logger().info('Position Window reçu!')
        else:
            pass

    def poseInit (self,msg):
        if not(self.recu_pos_init):
            self.pos_init=(msg.x,msg.y,msg.theta)
            # if len(self.path)!=1:
            #     x,y,z=self.path[1]
            #     self.path[1]=(msg.x, y, z)
            self.recu_pos_init=True
            # if self.recu_pos_w or mode==0:
            #     self.wps = self.compute_path() #la variable globale wps représente le vecteur qui donne les objectifs à atteindre
            self.get_logger().info('Position Init reçu!')
        else:
            self.pose=msg

    def compute_path(self):
        waypoints = []
        if self.graph==[]:
            for x,y,z in self.path:
                wp = Point() #réécriture des duos de floats sous forme du type de la requête à envoyer 
                wp.x = x
                wp.y = y  
                wp.z = z 
                waypoints.append(wp) #ajout du dernier point (dans le bon type) au nouveau vecteur qui donne les objectifs à atteindre
        else:
            waypoints=self.graph
            self.get_logger().info(f"waypoints")
        return waypoints

    def send_waypoints(self,msg):
        if mode:
            while not(self.recu_pos_w):
                sleep(0.1)
        while not(self.recu_pos_init):
            sleep(0.1)
        self.wps = self.compute_path()

        self.lead = msg.leader
        self.get_logger().info(f"Go ! leader {self.lead}")

        if self.lead :
            wp = self.wps[0]
            self.send_util(wp.x,wp.y,wp.z)
            newMap=Map()
            newMap.graph=self.graph[::4]   #on garde un wp sur 3
            self.publisher_done.publish(newMap)  
            wp = self.wps[1]
            self.send_util(wp.x,wp.y,wp.z)
        else:
            
            altitude=float(msg.nb-1)/1.0
            self.get_logger().info(f"altitude {altitude}")
            if self.formation:
                for wp in self.wps:          #on suit le graph
                    if self.repli:
                        return
                    self.send_util(wp.x,wp.y,wp.z+altitude)
                

                if mode:
                    for i in range (msg.nb-1,0,-1):
                        self.send_util(self.posWindow[0],self.posWindow[1] -0.5 ,self.posWindow[2]+float(i-1))
                    self.send_util(self.posWindow[0],self.posWindow[1],self.posWindow[2])
                    self.send_util(self.pos_init[0],self.posWindow[1] +1.5 ,self.posWindow[2])
                else:
                    for i in range (msg.nb-1,0,-1):
                        self.send_util(0.0,5.0 -0.5 ,1.5 +float(i-1))
                    self.send_util(0.0,5.0,1.0)
                    self.send_util(self.pos_init[0],6.5,1.0)
                newMap=Map()
                newMap.graph=self.graph[::3]   #on garde un wp sur 3
                self.publisher_done.publish(newMap)  #je suis arrivé
            else:
                wp=self.wps.pop(0)
                self.send_util(wp.x,wp.y,wp.z+altitude)
                self.formation = True          #car la prochaine fois que l'on appel GO, on sait qu'on sera en formation
                rd=Bool()
                self.publisher_ready.publish(rd)
                self.get_logger().info(f"TEST TEST TEST")

            # rd=Bool()
            # self.publisher_ready.publish()
            # while not(self.formation):
            #     sleep(0.2)

            

        
    def send_util(self,x,y,z):
        wp_r = Position3D.Request()
        wp_r.point.x = x
        wp_r.point.y = y  
        wp_r.point.z = z 
        self.set_goal(wp_r)
        self.get_result(Trigger.Request())

    def set_goal(self, request):
        future = self.client_goal.call_async(request) #Envoie la requête contenant le prochain objectif à local_path_node, future.result deviendra True quand le serveur aura répondu ""
        rclpy.spin_until_future_complete(self, future, executor=None) #Tourne en rond car pas d'executor spécifié en attendant que future.result soit True
        return future.result()
    
    def graph_build (self,msg):
        if self.lead:
            wp = Point()
            wp.x = msg.pose.position.x
            wp.y = msg.pose.position.y  
            wp.z = msg.pose.position.z
            self.graph.append(wp)

    def update_graph (self,msg):
        self.graph = msg.graph 
        #self.get_logger().info(f'Le leader est arrivé ! {self.graph}')

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
