import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist, Point
from tortues.pid_lib import PID
import math
from time import sleep

id=3
nb_drones=4

class Turtle3_Node(Node):                                   #modifier
    def __init__(self):
        super().__init__(f'Turtle{id}_Node')  # Nom du nœud          #modifier
        self.target=[10,3,0]                                    #modifier
        self.v=PID(2,0,0)
        self.theta=PID(2,0,0)
        #self.z=PID(1,1,1)
        self.turtleID = float(id)           #modifier
        self.turtleScore = 5.0      #modifier
        self.curr_iter = 0.0
        self.bestTurtle = Point()
        self.bestTurtle.x = self.turtleID # ID
        self.bestTurtle.y = self.turtleScore # score
        self.bestTurtle.z = self.curr_iter # score
        
        self.buff_vois1=[]
        self.buff_vois2=[]
        self.iter_max  = 2
        #self.hisTurtle = {}

        self.cl_group = ReentrantCallbackGroup()

        self.free=True

        self.publisher = self.create_publisher(Point, f'/turtle{id}/bestTurtle', 10)  #modifier*


        self.subscription1 = self.create_subscription(Point,f'/turtle{((id-1)-1)%nb_drones+1}/bestTurtle',self.listener_callback_vois1,10, callback_group= self.cl_group)  #modifier
        self.subscription2 = self.create_subscription(Point,f'/turtle{((id+1)-1)%nb_drones+1}/bestTurtle' ,self.listener_callback_vois2,10, callback_group= self.cl_group)  #modifier

        sleep(0.5)
        self.publisher.publish(self.bestTurtle)  # Publie le message        

        self.timer_maj   = self.create_timer(0.1, self.maj)

        self.cmd = self.create_publisher(Twist, f'/turtle{id}/cmd_vel', 10)  #modifier
        self.where = self.create_subscription(Pose,f'/turtle{id}/pose',self.listener_callback,10)  #modifier


    def listener_callback_vois1(self, msg):
        # while not(self.free):
        #     sleep(0.01)
        self.buff_vois1.append(msg)
        
    
    def listener_callback_vois2(self, msg):
        # while not(self.free):
        #     sleep(0.01)
        self.buff_vois2.append(msg)

     
    def maj(self):
        
        if self.curr_iter <= self.iter_max:
            self.free=False
            if self.buff_vois1 and self.buff_vois2:
                msg_vois1=self.buff_vois1.pop(0)
                msg_vois2=self.buff_vois2.pop(0)

                self.free=True

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
            self.timer_maj.cancel()
        self.free=True
        
    


    def publish_message(self,pos):

        if self.curr_iter > self.iter_max and self.turtleID == self.bestTurtle.x:

            send = Twist()
            err_x = self.target[0] - pos.x
            err_y = self.target[1] - pos.y
            err_pos = math.sqrt(err_x**2 + err_y**2)
            if err_pos > 0.01 :
                self.arrived=False

                v = self.v.calcul(err_pos)

                err_theta = math.atan2(err_y, err_x) - pos.theta
                
                send.linear.x = v * math.cos(err_theta)
                send.linear.y = v * math.sin(err_theta)
                send.angular.z = self.theta.calcul(err_theta)
            else:
                self.arrived=True
                self.get_logger().info(f'Je suis arrivé !')
            self.cmd.publish(send)  # Publie le message
            self.get_logger().info(f'Publié : "{send}"')
    
    def listener_callback(self, msg):
        #self.get_logger().info(f'Reçu : "{msg}"')  # Affiche le message reçu
        self.publish_message(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Turtle3_Node()  # Création du nœud                      #modifier
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    #rclpy.spin(node)  # Exécution du nœud
    executor.spin()
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()