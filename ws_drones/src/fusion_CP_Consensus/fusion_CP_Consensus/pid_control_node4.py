#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
#import des types qui serviront aux topics
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
#import de bibliotheques ou classes pour des besoins spécifiques
from fusion_CP_Consensus.pid_class import PID #on importe la classe dans laquelle on a délocalisé le calcul de PID
import math

id=int(__file__[-4])
nb_drones=4

class PID_Control(Node):
    def __init__(self):
        super().__init__('pid_control_node')

        #déclaration et assignation de paramètres
        self.declare_parameter('kp_lin', 1.0)
        self.declare_parameter('kp_ang', 2.0)
        kp_lin = self.get_parameter('kp_lin').value
        kp_ang = self.get_parameter('kp_ang').value
        
        #création de variables globales
        self.pid_v     = PID( kp = kp_lin )
        self.pid_theta = PID( kp = kp_ang )
        self.pose = Pose()
        self.pose_d = Pose()
        self.start = False

        #abonnement et création de topicsh
        self.subscription = self.create_subscription(Pose,f'/turtle{id}/pose', self.listener_cb_pose,10)
        self.subscription1 = self.create_subscription(Pose,f'/turtle{id}/pose_d', self.listener_cb_pose_d,10)
        self.publisher = self.create_publisher(Twist, f'/turtle{id}/cmd_vel', 10) 

        self.get_logger().info('Le nœud est démarré !')


    def listener_cb_pose_d(self, pose_d):
        self.get_logger().info(f"Tor{id} : {pose_d} reçu")
        self.start = True
        self.pose_d = pose_d

    def listener_cb_pose(self, pose):
        if not self.start:
            return
        self.pid_v.kp = self.get_parameter('kp_lin').value
        self.pid_theta.kp = self.get_parameter('kp_ang').value
        cmd_vel = Twist()         
        err_x = self.pose_d.x - pose.x
        err_y = self.pose_d.y - pose.y
        err_pose = math.sqrt(err_x**2+err_y**2)
        if abs(err_pose) > 0.1:

            v = self.pid_v.run(err_pose)
            err_theta = math.atan2(err_y, err_x) - pose.theta
            
            cmd_vel.linear.x = v * math.cos(err_theta)
            cmd_vel.linear.y = v * math.sin(err_theta)
            cmd_vel.angular.z = self.pid_theta.run(err_theta)
        
        self.publisher.publish(cmd_vel)
        
            
            
        




def main(args=None):
    rclpy.init(args=args)
    node = PID_Control()  # Création du nœud
    rclpy.spin(node)  # Exécution du nœud
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()