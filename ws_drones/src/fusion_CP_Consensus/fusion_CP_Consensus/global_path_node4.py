#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
#import des types qui serviront aux services
from example_interfaces.srv import Trigger
from turtlesim.srv import TeleportAbsolute
#import des types qui serviront aux topics
from std_msgs.msg import Bool
#import de bibliotheques pour des besoins spécifiques
from time import sleep

id=int(__file__[-4])
nb_drones=4

class global_path(Node):
    def __init__(self):
        super().__init__('global_path_node')

        #appel de fonctions à l'initialisation
        self.wps = self.compute_path() #la variable globale wps représente le vecteur qui donne les objectifs à atteindre

        self.client_goal = self.create_client(TeleportAbsolute, f'/turtle{id}/set_target_pose') #global_path_node est un client du service set_target_pose proposé par local_path_node
        self.client_result = self.create_client(Trigger, f'/turtle{id}/set_result') #global_path_node est un client du service set_result proposé par local_path_node
        self.__wait_services() 
        self.subscription_go = self.create_subscription(Bool, f'/turtle{id}/go',self.send_waypoints, 10)        



    def __wait_services(self): # méthode privée pour attendre que les deux serveurs de local_path_node soient accessibles, avant de continuer
        wait_goal_service = self.client_goal.wait_for_service(timeout_sec=1.0)
        wait_result_service = self.client_result.wait_for_service(timeout_sec=1.0)
        while not wait_goal_service or not wait_result_service :
            wait_goal_service = self.client_goal.wait_for_service(timeout_sec=1.0)
            wait_result_service = self.client_result.wait_for_service(timeout_sec=1.0)
            self.get_logger().info('Services not available, waiting...')

    def compute_path(self):
        path = [(1.0 , 1.0), #définition les objectifs à atteindre sous forme de vecteur de duos de floats
                (10.0, 1.0),
                (10.0, 10.0),
                (1.0 , 10.0),
                (1.0 , 1.0),
                ]
        waypoints = []
        for x,y in path:
            wp = TeleportAbsolute.Request() #réécriture des duos de floats sous forme du type de la requête à envoyer 
            wp.x = x
            wp.y = y  
            waypoints.append(wp) #ajout du dernier point (dans le bon type) au nouveau vecteur qui donne les objectifs à atteindre
        return waypoints

    def send_waypoints(self, msg):
        self.get_logger().info(f"Tor{id} : info {msg.data}")
        if msg.data :
            for wp in self.wps:
                #self.get_logger().info(f"Tor{id} : GO {wp}")
                self.set_goal(wp)
                self.get_result(Trigger.Request())

    def set_goal(self, request):
        self.get_logger().info(f"Tor{id} : colis envoyé")
        future = self.client_goal.call_async(request) #Envoie la requête contenant le prochain objectif à local_path_node, future.result deviendra True quand le serveur aura répondu ""
        rclpy.spin_until_future_complete(self, future, executor=None) #Tourne en rond car pas d'executor spécifié en attendant que future.result soit True
        self.get_logger().info(f"Tor{id} : réponse reçu")
        return future.result()
    
    """--------------------------------------Précisions sur set_goal et get_result---------------------------------------------
    call_async(request) : Make a service request and asyncronously get the result.Return type : Future.(A future completes when the request does)
    future est un type de variable très spéciale qui aloue de l'espace vide dans la mémoire qui attend une réponse asynchrone et s'actualisera tout seul au moment venu"""
        
    def get_result(self, request):
        self.get_logger().info(f"Tor{id} : départ demandé")
        future = self.client_result.call_async(request) #Envoie une requête vide pour demander à local_path_node si on est bien arrivé à l'objectif précédent
        rclpy.spin_until_future_complete(self, future, executor=None) #Tourne en rond car pas d'executor spécifié en attendant que future.result soit True
        self.get_logger().info(f"Tor{id} : arrivé à destination")
        return future.result()

def main(args=None):
    rclpy.init(args=args)
    node = global_path()  # Création du nœud
    rclpy.spin(node)  # Exécution du nœud
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()
