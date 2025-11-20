#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
#import des types qui serviront aux topics
from geometry_msgs.msg import Point
from std_msgs.msg import Bool
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

# on récupère l'id du drone
id=int(__file__[-4])


class global_path(Node):
    def __init__(self):
        super().__init__('global_path_node')

        ############## max consensus init ##############

        self.turtleID     = float(id) 
        self.turtleScore  = 5.0-float(id)    #float(random.randrange(0,50,1))  #score aléatoire entre 0 et 50
        self.curr_iter    = 0.0
        self.bestTurtle   = Point()
        self.bestTurtle.x = self.turtleID # ID
        self.bestTurtle.y = self.turtleScore # score
        self.bestTurtle.z = self.curr_iter # itération actuelle
        
        self.gone          = False
        self.crash         = True
        #self.counter_crash = 0

        self.buff_vois1   = []
        self.buff_vois2   = []
        self.iter_max     = nb_drones//2  #uniquement valable en communication "circulaire"

        self.__create_topics()
        sleep(0.5)
        self.publisher.publish(self.bestTurtle)  # Publie le premier message

        self.timer_maj     = self.create_timer(0.1, self.maj)  # Lance la boucle de publication de mise à jour
        self.timer_refresh = self.create_timer(3, self.refresh)  # Refresh après 3sec au cas où max-consensus est crash
        ################################################

        self.get_logger().info('Le nœud est démarré !')

        
    
########################   MAX CONSENSUS   ###########################
    def __create_topics(self):
        self.cl_group      = ReentrantCallbackGroup()
        self.publisher     = self.create_publisher(Point, f'/turtle{id}/bestTurtle', 10)
        self.subscription1 = self.create_subscription(Point,f'/turtle{((id-1)-1)%nb_drones+1}/bestTurtle',self.listener_callback_vois1,10, callback_group= self.cl_group)
        self.subscription2 = self.create_subscription(Point,f'/turtle{((id+1)-1)%nb_drones+1}/bestTurtle' ,self.listener_callback_vois2,10, callback_group= self.cl_group)
        self.publisher_go  = self.create_publisher(Bool, f'/turtle{id}/go', 10)

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
                #self.get_logger().info(f"Tor{id} : itération :{self.curr_iter}")
                
                self.bestTurtle.z = self.curr_iter
                self.publisher.publish(self.bestTurtle)  # Publie le message
        
        else:
            self.crash = False   #cela signifi que le premier consensus n'a pas crash
            self.get_logger().info(f"Tor{id}: score {self.bestTurtle.y}")
            if self.bestTurtle.y == 0.0:   #si après le max-consensus on est à 0 c'est que tout le monde est parti
                self.timer_maj.cancel()
                self.timer_refresh.cancel()
                self.get_logger().info("Tout le monde est parti !")

            if not(self.gone) :  #si il n'est pas encore parti :
                if self.turtleID == self.bestTurtle.x:
                    go=Bool()
                    go.data=True
                    self.publisher_go.publish(go) # C'est parti !
                    self.turtleScore  = 0.0
                    self.gone = True
                else:
                    self.turtleScore  = float(random.randrange(0,50,1))  #on recalcul le score
                

            self.curr_iter    = 0.0
            self.bestTurtle.x = self.turtleID # ID
            self.bestTurtle.y = self.turtleScore # score
            self.bestTurtle.z = self.curr_iter # itération actuelle
            self.buff_vois1   = []
            self.buff_vois2   = []
            sleep(3)
            self.publisher.publish(self.bestTurtle)



    def refresh (self):
            if self.crash :
                self.curr_iter    = 0.0
                self.bestTurtle.x = self.turtleID # ID
                self.bestTurtle.y = self.turtleScore # score
                self.bestTurtle.z = self.curr_iter # itération actuelle
                self.publisher.publish(self.bestTurtle)
            self.timer_refresh.cancel()

######################################################################


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
