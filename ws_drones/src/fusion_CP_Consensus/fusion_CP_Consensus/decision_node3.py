#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
#import des types qui serviront aux topics
from geometry_msgs.msg import Point
from turtlesim.msg import Pose
from std_msgs.msg import Bool, Float32
from my_custom_interfaces.msg import Map, Go
#import de bibliotheques pour des besoins spécifiques
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from time import sleep
import random
import json
from pathlib import Path


# Utils.json pournombre de drones
dossier = Path(__file__).parent
dossier = dossier.parents[5]
utils = dossier/"src"/"fusion_CP_Consensus"/"utils.json" 
with open(utils) as f:
    file = json.load(f)

nb_drones=int(file["nb_drones"])
mode=int(file["mode"]) #On récupère l'information du mode : 0=Simu, 1=Réel
aleatoire=False  #En attendant 

# on récupère l'id du drone
id=int(__file__[-4])


class decision(Node):
    def __init__(self):
        super().__init__('decision')

        ############## max consensus init ##############

        self.turtleID     = float(id) 
        self.turtleScore  = 5.0-float(id) 
        if aleatoire:
            self.turtleScore = float(random.randrange(1,50,1))  #score aléatoire entre 1 et 50
        self.curr_iter    = 0.0
        self.bestTurtle   = Point()
        self.bestTurtle.x = self.turtleID # ID
        self.bestTurtle.y = self.turtleScore # score
        self.bestTurtle.z = self.curr_iter # itération actuelle
        
        self.err           = None
        self.repli         = False

        self.gone          = False
        self.crash         = True
        self.Leader        = True  #tant qu'on est pas parti on est potentiellement le leader
        self.formation_ok  = False
        self.leader_ok     = False
        self.nb            = 0
        self.phase         = 1    #Phase 1 : le leader ouvre la voie, trouve la fenêtre et si poste. Puis le reste des drones se mettent en formation.
                                    #Phase 2 : Elle est déclenchée si les drones suiveurs sont en formation. Ils se déplacent en formation jusqu'à la fenêtre, puis passe par celle-ci.
        self.buff_vois1   = []
        self.buff_vois2   = []
        self.iter_max     = nb_drones//2  #uniquement valable en communication "circulaire"

        self.__create_topics()
        sleep(0.5) #Pour ralentir le processus et éviter les échecs d'initialisation
        self.publisher.publish(self.bestTurtle)  # Publie le premier message

        self.timer_maj     = self.create_timer(0.2, self.maj)  # Lance la boucle de publication de mise à jour
        self.timer_refresh = self.create_timer(5, self.refresh)  # Refresh après 5sec au cas où max-consensus ai crash
        ################################################

        self.get_logger().info('Le nœud est démarré !')

        
    
########################   MAX CONSENSUS   ###########################
    def __create_topics(self):
        #qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.cl_group      = ReentrantCallbackGroup()
        self.publisher          = self.create_publisher(Point, f'/turtle{id}/bestTurtle', 10)
        self.subscription1      = self.create_subscription(Point,f'/turtle{((id-1)-1)%nb_drones+1}/bestTurtle',self.listener_callback_vois1,10, callback_group= self.cl_group)
        self.subscription2      = self.create_subscription(Point,f'/turtle{((id+1)-1)%nb_drones+1}/bestTurtle' ,self.listener_callback_vois2,10, callback_group= self.cl_group)
        self.publisher_go       = self.create_publisher(Go, f'/turtle{id}/go', 10)
        self.subscriptionLead   = self.create_subscription(Map,'/leader/done',self.listener_callback_Leader,10)
        self.subscription_ready = self.create_subscription(Bool, f'/turtle{id}/ready',self.ready,10)
        self.subscription_repli = self.create_subscription(Bool, f'/repli', self.repli_update, 10)
        self.dist_init          = self.create_subscription(Float32,f'/turtle{id}/err_dist',self.err_update, 10,callback_group=self.cl_group)
        self.publisher_repli_go = self.create_publisher(Go, f'/turtle{id}/repli', 10)

    def listener_callback_vois1(self, msg):
        self.buff_vois1.append(msg)
        
    def listener_callback_vois2(self, msg):
        self.buff_vois2.append(msg)


    def err_update(self, msg):
        self.err=msg.data
    
    def maj(self):
        if self.curr_iter <= self.iter_max:
            if self.phase == 1 or (self.phase == 2 and (self.formation_ok or self.Leader)):
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
                    #self.get_logger().info(f"Tor{id} : itération :{self.curr_iter}")
                    
                    self.bestTurtle.z = self.curr_iter
                    self.publisher.publish(self.bestTurtle)  # Publie le message
        
        else:
            self.crash = False   #cela signifi que le premier consensus n'a pas crash
            
            #self.get_logger().info(f"Tor{id}: score {self.bestTurtle.y}")
            if self.phase == 2 and self.formation_ok:
                go=Go()
                go.leader=self.Leader
                go.nb=self.nb
                self.publisher_go.publish(go) # C'est parti !
                self.get_logger().info("Go 2!")
                #self.timer_maj.cancel()

            else:
                if self.repli:
                    if self.turtleID == self.bestTurtle.x:
                        go=Go()
                        go.leader=self.Leader
                        go.nb=self.nb
                        self.publisher_repli_go.publish(go)
                        self.get_logger().info("Repli Go!")
                    else:
                        self.turtleScore  = 1024.0-self.err#float(random.randrange(1,50,1))  #on calcul le score pour ceux qui passent dans la fenêtre
                        self.nb+=1

                elif self.bestTurtle.y == 0.0:   #si après le max-consensus on est à 0 c'est que tout le monde est parti
                    # self.timer_maj.cancel()
                    # self.timer_refresh.cancel()
                    self.get_logger().info("Tout le monde est prêt ?")
                    
                    self.bestTurtle.x = self.turtleID # ID
                    self.bestTurtle.y = 0.0 # score
                    self.bestTurtle.z = 0.0 # itération actuelle
                    # self.publisher.publish(self.bestTurtle)
                    self.phase = 2                                     #On déclenche la phase 2
                    
                elif not(self.gone) :  #si il n'est pas encore parti :
                    if self.turtleID == self.bestTurtle.x:
                        go=Go()
                        go.leader=self.Leader
                        go.nb=self.nb
                        self.publisher_go.publish(go) # C'est parti !
                        self.get_logger().info("Go !")
                        self.turtleScore  = 0.0
                        self.gone         = True
                    else:
                        self.Leader       = False #On est pas parti en premier donc on n'est pas leader
                        self.turtleScore  = 5.0-float(id) 
                        if aleatoire:
                            self.turtleScore = float(random.randrange(1,50,1))  #score aléatoire entre 1 et 50
                        self.nb+=1
                        #self.get_logger().info(f"nb {self.nb}")

                self.curr_iter    = 0.0
                self.bestTurtle.x = self.turtleID # ID
                self.bestTurtle.y = self.turtleScore # score
                self.bestTurtle.z = self.curr_iter # itération actuelle
                self.buff_vois1   = []
                self.buff_vois2   = []

                sleep(1)                                 #à modifier
                if (not(self.Leader) and self.leader_ok) or self.phase == 2 or self.repli:  #not(self.Leader) and 
                    self.publisher.publish(self.bestTurtle)
                    self.get_logger().info(f"Publi, nb {self.nb}")
            
    def listener_callback_Leader (self,msg):
        self.get_logger().info(f"Ok le leader est arrivé")
        self.publisher.publish(self.bestTurtle)
        self.leader_ok = True

    def ready (self,msg):
        self.formation_ok = True

    def repli_update (self,msg):
        self.repli=True
        self.get_logger().info(f"Repli !")

        self.turtleScore  = 1024.0-self.err
        self.curr_iter    = 0.0
        self.bestTurtle.x = self.turtleID # ID
        self.bestTurtle.y = self.turtleScore # score
        self.bestTurtle.z = self.curr_iter # itération actuelle
        self.buff_vois1   = []
        self.buff_vois2   = []
        self.publisher.publish(self.bestTurtle)


    def refresh (self):
            if self.crash :
                self.curr_iter    = 0.0
                self.bestTurtle.x = self.turtleID # ID
                self.bestTurtle.y = self.turtleScore # score
                self.bestTurtle.z = self.curr_iter # itération actuelle
                self.publisher.publish(self.bestTurtle)
            self.get_logger().info('Refresh...')
            self.timer_refresh.cancel()
            

######################################################################


def main(args=None):
    rclpy.init(args=args)
    node = decision()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
