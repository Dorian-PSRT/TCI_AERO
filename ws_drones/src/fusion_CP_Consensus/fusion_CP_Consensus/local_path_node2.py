#import des bibliotheques ROS2
import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node
#import des types qui serviront aux topics
from turtlesim.msg import Pose
from geometry_msgs.msg import Point, PoseStamped
#import des types qui serviront aux services
from my_custom_interfaces.srv import Position3D
from my_custom_interfaces.msg import PosObstacles
from example_interfaces.srv import Trigger
#import de bibliotheques pour des besoins spécifiques
import numpy as np  #sert pour utiliser des vecteurs
import threading    #permet de lancer plusieurs fonctions en parallèle
import json
from pathlib import Path
from fusion_CP_Consensus.champs_pot_class import CP


# Utils.json pournombre de drones
dossier = Path(__file__).parent
dossier = dossier.parents[5]
utils = dossier/"src"/"fusion_CP_Consensus"/"utils.json" 
with open(utils) as f:
    file = json.load(f)

nb_drones=int(file["nb_drones"])

# on récupère l'id du drone
id=int(__file__[-4])


class local_path(Node):
    def __init__(self):
        super().__init__('local_path_node')


        #création de variables globales
        self.start     = False
        self.pose      = Pose()
        self.obstacles = []
        self.period    = 0.5
        self.c         = 0.0 

        #appel de fonctions à l'initialisation
        self.__create_topics()

        self.get_logger().info('Le nœud est démarré !')
    
    def __create_topics(self): #méthode privée qui regroupe les déclarations faites à l'initialisation
        self.cl_group = ReentrantCallbackGroup() #outil de ROS2 appeler les fonctions dans ce groupe en parrallèle avec un callback(prioritaire en temps normal)
        self.thread_event = threading.Event() #outil de python pour utiliser les interruptions (dans ce cas : à arrivée de la tortue à l'objectif)
        self.subscription = self.create_subscription(Pose,f'/turtle{id}/pose', self.listener_callback,10, callback_group= self.cl_group) #abonnement au topic pose publié par turtlesim_node en précisant callback_group de sorte que la récupérations des données se fasse en parralèlle d'autres actions
        #self.publisher    = self.create_publisher(Point, f'/turtle{id}/pose_d', 10) #publication dans pose_d du prochain pas à faire à destination de pid_control_node
        self.publisher    = self.create_publisher(PoseStamped, f'/Crazyflie{id}/pose_d', 10)
        self.timer        = self.create_timer(0.01, self.set_pose_d) #création d'un timer qui appel la fonction set_pose_d chaque 0.1 s
        self.service      = self.create_service(Position3D, f'/turtle{id}/set_target_pose', self.handle_goal_request) #local_path_node a un serveur set_target_pose à destination de global_path_node
        self.service_r    = self.create_service(Trigger, f'/turtle{id}/set_result', self.handle_result_request, callback_group= self.cl_group)  #local_path_node a un serveur set_result à destination de global_path_node
        self.getobstacles = self.create_subscription(PosObstacles,'OptiTrack/obstacles',self.get_obstacles,10, callback_group= self.cl_group)

    def get_obstacles(self,obst_new):
        moi=obst_new.flotants.pop(id-1)      # ATTENTION : on retire l'obstacle de soit même. Le drône est un obstacle pour les autres mais pas pour soit même
        self.obstacles  = obst_new.fixes+obst_new.flotants
        #self.get_logger().info(f'obstacle poped: CF {id} : {moi}')
   

    def handle_goal_request(self, request, response):
        self.pose_goal = request            #la variable globale pose_goal (créée ici) correspond au prochain objectif fixé par global_path_node à travers le service set_target_pose
        #self.get_logger().info(f'position reçue par local : x={self.pose_goal.point.x}, y={self.pose_goal.point.y}, z={self.pose_goal.point.z}')
        #response.success = True
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

    def set_pose_d(self):       #fonction appelée par un timer toutes les 0.1s
        if self.c >= self.period :
            self.c = 0.0
            if not self.start:      #si l'autorisation de démarer n'a pas été donnée on sort directement de la fonction
                #self.publisher.publish(self.pose)
                return
            nav=CP()
            if abs(nav.norme_erreur(self.pose_goal, self.pose)[0]) > 0.2:   #pour preshot l'arrivée à la cible
                if abs(nav.norme_erreur(self.pose_goal, self.pose)[0]) > 0.2:
                    prochain_pas,self.period = nav.set_next_step(self.pose_goal, self.pose, self.obstacles)
                    
                    self.get_logger().info(f"Prochain pas :({prochain_pas[0]} {prochain_pas[1]})")
                    

                    pose_d_ = np.array([self.pose.x, self.pose.y]) + prochain_pas   #somme de la position actuelle et du prochain pas à faire (multiplié par un gain) pour obtenir la prochaine position

                    """-------------Précision sur le calcul de la prochaine position locale à atteindre---------------"
                    La ligne de code ci dessus sera adaptée pour être modulaire. Actuellement on utilise la méthode des champs potentiels pour connaitre le prochain pas à faire
                    , mais on pourrait utiliser une autre méthode, ainsi il suffirait de remplacer la partie qu'on aditionne à la position actuelle pour obtenir la prochaine position différement"""
                    
                    pose_d_point = Point() #déclaration de la variable locale pose_d avec le type Pose
                    pose_d_point.x = pose_d_[0] #changement de type de la prochaine position (le vecteur étant utilisé pour la méthode des champs potentiels)
                    pose_d_point.y = pose_d_[1]
                    pose_d_point.z = 1.5

                    pose_d = PoseStamped()
                    pose_d.pose.position = pose_d_point

                    self.publisher.publish(pose_d)
                else:
                    self.start =False       #on annonce la fin du déplacement
                    pointactuel = Point()
                    pointactuel.x = self.pose.x
                    pointactuel.y = self.pose.y
                    pointactuel.z = 1.5

                    pointactuel_ps = PoseStamped()
                    pointactuel_ps.pose.position = pointactuel

                    self.publisher.publish(pointactuel_ps) #la prochaine position est celle à laquelle on est déjà

            else:                       #si on est arrivé
                self.thread_event.set() #active l'interruption qui correspond à l'arrivée prochaine à l'objectif
        else :
            self.c += 0.01

        


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor() #permet de lancer plusieurs fonctions en parallèle
    node = local_path()  # Création du nœud
    executor.add_node(node)
    #rclpy.spin(node)  # Exécution du nœud
    executor.spin()
    
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()