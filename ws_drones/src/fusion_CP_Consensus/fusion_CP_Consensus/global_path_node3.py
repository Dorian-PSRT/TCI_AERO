#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
#import des types qui serviront aux services
from my_custom_interfaces.srv import Position3D
from example_interfaces.srv import Trigger
from turtlesim.srv import TeleportAbsolute
#import des types qui serviront aux topics
from std_msgs.msg import Bool
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

# on récupère l'id du drone
id=int(__file__[-4])


class global_path(Node):
    def __init__(self):
        super().__init__('global_path_node')

        #appel de fonctions à l'initialisation
        self.wps = self.compute_path() #la variable globale wps représente le vecteur qui donne les objectifs à atteindre
        
        client_cb_group = None
        topic_cb_group  = MutuallyExclusiveCallbackGroup()  #hyper important, ça permet d'appeler un service dans un callback ! (sinon ça casse tout)

        self.subscription_go = self.create_subscription(Bool, f'/turtle{id}/go',self.send_waypoints, 10,callback_group=topic_cb_group)

        self.client_goal = self.create_client(Position3D, f'/turtle{id}/set_target_pose',callback_group=client_cb_group) #global_path_node est un client du service set_target_pose proposé par local_path_node
        self.client_result = self.create_client(Trigger, f'/turtle{id}/set_result',callback_group=client_cb_group) #global_path_node est un client du service set_result proposé par local_path_node
        self.__wait_services() 

        #self.subscription_go = self.create_subscription(Bool, f'/turtle{id}/go',self.send_waypoints, 10,callback_group=topic_cb_group)

        self.get_logger().info('Le nœud est démarré !')

    def __wait_services(self): # méthode privée pour attendre que les deux serveurs de local_path_node soient accessibles, avant de continuer
        wait_goal_service   = self.client_goal.wait_for_service(timeout_sec=1.0)
        wait_result_service = self.client_result.wait_for_service(timeout_sec=1.0)
        while not wait_goal_service or not wait_result_service :
            wait_goal_service   = self.client_goal.wait_for_service(timeout_sec=1.0)
            wait_result_service = self.client_result.wait_for_service(timeout_sec=1.0)
            self.get_logger().info('Services not available, waiting...')

    def compute_path(self):
        # path = [(0.0 , 5.0 , 1.5), #définition les objectifs à atteindre sous forme de vecteur de duos de floats
        #         (-5.0, 8.0 , 2.0), #+2.0*float(id)
        #         ]
        path = [(2.0, float(id)-1.0 , 1.0), #définition les objectifs à atteindre sous forme de vecteur de duos de floats
                ]
        waypoints = []
        for x,y,z in path:
            wp = Position3D.Request() #réécriture des duos de floats sous forme du type de la requête à envoyer 
            wp.point.x = x
            wp.point.y = y  
            wp.point.z = z 
            waypoints.append(wp) #ajout du dernier point (dans le bon type) au nouveau vecteur qui donne les objectifs à atteindre
        return waypoints

    def send_waypoints(self,msg):
        if msg.data :
            for wp in self.wps:
                self.set_goal(wp)
                self.get_result(Trigger.Request())


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
