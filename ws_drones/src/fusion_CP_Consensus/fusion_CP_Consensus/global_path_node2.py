#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
#import des types qui serviront aux services
from example_interfaces.srv import Trigger
from turtlesim.srv import TeleportAbsolute
#import des types qui serviront aux topics
from geometry_msgs.msg import Point
#import de bibliotheques pour des besoins spécifiques
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from time import sleep

id=int(__file__[-4])
nb_drones=4

class global_path(Node):
    def __init__(self):
        super().__init__('global_path_node')

        self.client_goal = self.create_client(TeleportAbsolute, f'/turtle{id}/set_target_pose') #global_path_node est un client du service set_target_pose proposé par local_path_node
        self.client_result = self.create_client(Trigger, f'/turtle{id}/set_result') #global_path_node est un client du service set_result proposé par local_path_node
        
        #appel de fonctions à l'initialisation
        self.__wait_services() 
        self.wps = self.compute_path() #la variable globale wps représente le vecteur qui donne les objectifs à atteindre
        
        ############## max consensus init ##############

        self.turtleID = float(id) 
        self.turtleScore = 25.0      #modifier
        self.curr_iter = 0.0
        self.bestTurtle = Point()
        self.bestTurtle.x = self.turtleID # ID
        self.bestTurtle.y = self.turtleScore # score
        self.bestTurtle.z = self.curr_iter # itération actuelle
        
        self.buff_vois1=[]
        self.buff_vois2=[]
        self.iter_max  = nb_drones//2  #uniquement valable en communication "circulaire"

        self.__create_topics()
        sleep(0.5)
        self.publisher.publish(self.bestTurtle)  # Publie le premier message

        self.timer_maj   = self.create_timer(0.1, self.maj)  # Lance la boucle de publication de mise à jour
        ################################################
        
    
########################   MAX CONSENSUS   ###########################
    def __create_topics(self):
        self.cl_group = ReentrantCallbackGroup()
        self.publisher = self.create_publisher(Point, f'/turtle{id}/bestTurtle', 10)
        self.subscription1 = self.create_subscription(Point,f'/turtle{((id-1)-1)%nb_drones+1}/bestTurtle',self.listener_callback_vois1,10, callback_group= self.cl_group)
        self.subscription2 = self.create_subscription(Point,f'/turtle{((id+1)-1)%nb_drones+1}/bestTurtle' ,self.listener_callback_vois2,10, callback_group= self.cl_group)


    def listener_callback_vois1(self, msg):
        self.buff_vois1.append(msg)
        
    
    def listener_callback_vois2(self, msg):
        self.buff_vois2.append(msg)

     
    def maj(self):
        if self.curr_iter <= self.iter_max:
            if self.buff_vois1 and self.buff_vois2:
                msg_vois1=self.buff_vois1.pop(0)
                msg_vois2=self.buff_vois2.pop(0)


                if msg_vois1.y > self.bestTurtle.y :   # si le voisin 1 a un meilleur score
                    self.bestTurtle.x = msg_vois1.x
                    self.bestTurtle.y = msg_vois1.y
                if msg_vois2.y > self.bestTurtle.y :   # si le voisin 2 a un meilleur score
                    self.bestTurtle.x = msg_vois2.x
                    self.bestTurtle.y = msg_vois2.y
                
                self.curr_iter += 1
                self.get_logger().info(f"Tor{id} : itération :{self.curr_iter}")
                
                self.bestTurtle.z = self.curr_iter
                self.publisher.publish(self.bestTurtle)  # Publie le message
        else:
            self.send_waypoints(self.wps) # C'est parti, peut-être...
            self.timer_maj.cancel()
######################################################################

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

    def send_waypoints(self, waypoints):
        if self.turtleID == self.bestTurtle.x: #propre à Max Consensus : si la tortue est sélectionnée alors elle lance l'itinéraire
            for wp in waypoints:
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
    node = global_path()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
