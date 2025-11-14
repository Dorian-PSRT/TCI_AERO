#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
#import des types qui serviront aux topics
from geometry_msgs.msg import Point
from my_custom_interfaces.msg import PosObstacles
from turtlesim.msg import Pose
#import de bibliotheques ou classes pour des besoins spécifiques

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

        self.obstacles_flotants = [Point() for _ in range(nb_drones)]
        obst1=Point()
        obst1.x=5.5
        obst1.y=8.0
        obst2=Point()
        obst2.x=5.5
        obst2.y=3.0
        self.obstacles_fixes    = []

        self.subscription1 = self.create_subscription(Pose,'/turtle1/pose', self.pose1,10)
        self.subscription2 = self.create_subscription(Pose,'/turtle2/pose', self.pose2,10)
        self.subscription3 = self.create_subscription(Pose,'/turtle3/pose', self.pose3,10)
        self.subscription4 = self.create_subscription(Pose,'/turtle4/pose', self.pose4,10)
        self.timer         = self.create_timer(0.02, self.send_info)

        self.publisher = self.create_publisher(PosObstacles,'OptiTrack/obstacles',10)

        self.get_logger().info('Le nœud émulateur Opti Track est démarré !')

    def pose1 (self,pos): self.position (pos,1)
    def pose2 (self,pos): self.position (pos,2)
    def pose3 (self,pos): self.position (pos,3)
    def pose4 (self,pos): self.position (pos,4)

    def position (self,pos,i):
        pos_point=Point()
        pos_point.x=pos.x
        pos_point.y=pos.y
        pos_point.z=pos.z
        self.obstacles_flotants[i-1]=pos_point

    def send_info (self):
        obstacles          = PosObstacles()
        obstacles.fixes    = self.obstacles_fixes
        obstacles.flotants = self.obstacles_flotants
        #self.publisher.publish(obstacles)
        
            
            
        




def main(args=None):
    rclpy.init(args=args)
    node = fake_ot_node()  # Création du nœud
    rclpy.spin(node)  # Exécution du nœud
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()