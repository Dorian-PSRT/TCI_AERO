
#import des bibliotheques ROS2
import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from rclpy.node import Node
#import des types qui serviront aux topics
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Bool
#import des types qui serviront aux services
from turtlesim.srv import TeleportAbsolute
from example_interfaces.srv import Trigger
#import de bibliotheques pour des besoins spécifiques
import numpy as np  #sert pour utiliser des vecteurs
import threading    #permet de lancer plusieurs fonctions en parallèle
import math

class SimpleNode(Node):
    def __init__(self):
        super().__init__('local_path_node')

        #création de variables globales
        self.start = False
        self.pose = Pose()

        #appel de fonctions à l'initialisation
        self.__create_obstacles()
        self.__create_topics()

        self.get_logger().info('Le nœud est démarré !')
    
    def __create_topics(self): #méthode privée qui regroupe les déclarations faites à l'initialisation
        self.cl_group = ReentrantCallbackGroup() #outil de ROS2 appeler les fonctions dans ce groupe en parrallèle avec un callback(prioritaire en temps normal)
        self.thread_event = threading.Event() #outil de python pour utiliser les interruptions (dans ce cas : à arrivée de la tortue à l'objectif)
        self.subscription = self.create_subscription(Pose,'/turtle1/pose', self.listener_callback,10, callback_group= self.cl_group) #abonnement au topic pose publié par turtlesim_node en précisant callback_group de sorte que la récupérations des données se fasse en parralèlle d'autres actions
        self.publisher    = self.create_publisher(Pose, '/turtle1/pose_d', 10) #publication dans pose_d du prochain pas à faire à destination de pid_control_node
        self.timer        = self.create_timer(0.1, self.set_pose_d) #création d'un timer qui appel la fonction set_pose_d chaque 0.1 s
        self.service      = self.create_service(TeleportAbsolute, '/turtle1/set_target_pose', self.handle_goal_request) #local_path_node a un serveur set_target_pose à destination de global_path_node
        self.service_r    = self.create_service(Trigger, '/turtle1/set_result', self.handle_result_request, callback_group= self.cl_group)  #local_path_node a un serveur set_result à destination de global_path_node

    def __create_obstacles(self):
        
        obstacle  = np.array([3.0, 3.0])    #sert à définir les positions d'obstacles virtuels
        self.obstacles  = [obstacle]
        
    def handle_goal_request(self, request, response):
        self.pose_goal = request            #la variable globale pose_goal (créée ici) correspond au prochain objectif fixé par global_path_node à travers le service set_target_pose
        return response

    def handle_result_request(self, request, response): #fonction précisé en callback_group de sorte qu'elle se fasse en parralèlle de la réupération de données par listener_callback
        self.start = True                   #lorsqu'on reçoit la requête vide de globa_path_node pour demander si on est bien arrivé à l'objectif précédent on autorise le démarrage du déplacement
        self.thread_event.clear()           #réinitialisations des interuptions
        statut = self.thread_event.wait(timeout=200) #attend pendant 200 s qu'une interruption annonce l'arrivée à l'objectif actuel
        if statut: 
            response.success = True
        else:      
            response.success = False
        self.start = False                  #si l'interuption a eu lieu ou si les 200 s se sont écoulés on annonce la fin du déplacement
        return response

    def listener_callback(self, pose):
        self.pose = pose                    #récupérations des données du topic pose publié par turtlesim_node en parralèlle d'autres actions (callback_group)

    def force_attr(self, goal, pose, k):
        err = np.array([goal.x, goal.y]) - np.array([pose.x, pose.y])
        err_pose = np.linalg.norm(err)
        f_attr = k * err
        return f_attr, err_pose

    def force_repu(self, obstacles, pose_robot, k = 100.0, d_0 = 2.0):
        f_repu = np.array([0.0, 0.0])
        pose = np.array([pose_robot.x, pose_robot.y])
        for obs in obstacles:
            err = pose - obs  
            d = np.linalg.norm(err) - 1.0

            if d <= 0:
                grad_d = err / np.linalg.norm(err)
                f_repu += k*(1/d_0)**2*(1/d-1/d_0)*grad_d
                
            elif d < d_0:
                grad_d = err / np.linalg.norm(err)
                f_repu += (k/d**2)*(1/d-1/d_0)*grad_d
                
            else:
                f_repu += np.array([0.0, 0.0])

        return f_repu
        

    def set_pose_d(self):       #fonction appelée par un timer toutes les 0.1s
        if not self.start:      #si l'autorisation de démarer n'a pas été donnée on sort directement de la fonction
            #self.publisher.publish(self.pose)
            return
        
        f_attr, err_pose = self.force_attr(self.pose_goal, self.pose, k= 10.0) #appel de la fonction force_attr
        
        
        if abs(err_pose) > 0.1:
            f_repu = self.force_repu(self.obstacles, self.pose, k = 10.0, d_0 = 3.0)    #si on n'est pas encore arrivé on appel force_repu
            F = f_attr + f_repu                                                         #le vecteur qui défini le prochain pas correspond à la sommes des vecteurs de forces atractives et répulsives
            pose_d_ = np.array([self.pose.x, self.pose.y]) + 2.0 * F/np.linalg.norm(F)  #somme de la position actuelle et du prochain pas à faire (multiplié par un gain) pour obtenir la prochaine position

            """-------------Précision sur le calcul de la prochaine position locale à atteindre---------------"
            La ligne de code ci dessus sera adaptée pour être modulaire. Actuellement on utilise la méthode des champs potentiels pour connaitre le prochain pas à faire
            , mais on pourrait utiliser une autre méthode, ainsi il suffirait de remplacer la partie qu'on aditionne à la position actuelle pour obtenir la prochaine position différement"""
            
            pose_d = Pose() #déclaration de la variable locale pose_d avec le type Pose
            pose_d.x = pose_d_[0] #changement de type de la prochaine position (le vecteur étant utilisé pour la méthode des champs potentiels)
            pose_d.y = pose_d_[1] 
            self.publisher.publish(pose_d)

        else:                       #si on est arrivé
            self.start =False       #on annonce la fin du déplacement
            self.thread_event.set() #active l'interruption qui correspond à l'arrivée à l'objectif
            self.publisher.publish(self.pose) #la prochaine position est celle à laquelle on est déjà

        


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor() #permet de lancer plusieurs fonctions en parallèle
    node = SimpleNode()  # Création du nœud
    executor.add_node(node)
    #rclpy.spin(node)  # Exécution du nœud
    executor.spin()
    
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()