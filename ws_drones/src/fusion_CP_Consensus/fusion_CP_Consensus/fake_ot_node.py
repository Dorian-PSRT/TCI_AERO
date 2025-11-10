#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
#import des types qui serviront aux topics
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
#import de bibliotheques ou classes pour des besoins spécifiques
from fusion_CP_Consensus.pid_class import PID #on importe la classe dans laquelle on a délocalisé le calcul de PID
import math
import json
from pathlib import Path

# Utils.json pournombre de drones
dossier = Path(__file__).parent
dossier = dossier.parents[5]
utils = dossier/"src"/"fusion_CP_Consensus"/"utils.json" 
with open(utils) as f:
    file = json.load(f)

nb_drones=int(file["nb_drones"])


class fake_ot_node(Node):
    def __init__(self):
        super().__init__('fake_ot_node')

        self.obstacles_flotants = []
        self.obstacles_fixes    = []

        self.subscription1 = self.create_subscription(Pose,'/turtle1/pose', self.pose(1),10)
        self.subscription2 = self.create_subscription(Pose,'/turtle2/pose', self.pose(2),10)
        self.subscription3 = self.create_subscription(Pose,'/turtle3/pose', self.pose(3),10)
        self.subscription4 = self.create_subscription(Pose,'/turtle4/pose', self.pose(4),10)
        self.timer         = self.create_timer(0.1, self.send_info)

        self.publisher = self.create_publisher(Pose,'OptiTrack/obstacles',10)

        self.get_logger().info('Le nœud émulateur Opti Track est démarré !')

    def pose (self,i,pos):
        self.obstacles_flotants[i-1]=(pos.x,pos.y)

    def send_info (self):
        self.publisher.publish(self.obstacles_flotants)
        
            
            
        




def main(args=None):
    rclpy.init(args=args)
    node = fake_ot_node()  # Création du nœud
    rclpy.spin(node)  # Exécution du nœud
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()