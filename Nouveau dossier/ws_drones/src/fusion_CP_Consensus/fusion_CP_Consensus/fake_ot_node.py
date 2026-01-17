#import des bibliotheques ROS2
import rclpy
from rclpy.node import Node
#import des types qui serviront aux topics
from geometry_msgs.msg import Point
from my_custom_interfaces.msg import PosObstacles
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseStamped
#import de bibliotheques ou classes pour des besoins spécifiques
from rclpy.qos import ReliabilityPolicy, QoSProfile

import json
from pathlib import Path

# Utils.json pournombre de drones
dossier = Path(__file__).parent
dossier = dossier.parents[5]
utils = dossier/"src"/"fusion_CP_Consensus"/"utils.json" 
with open(utils) as f:
    file = json.load(f)

nb_drones=int(file["nb_drones"])
mode=int(file["mode"])
obstacles_data=file["obstacles"]

class fake_ot_node(Node):
    def __init__(self):
        super().__init__('fake_ot_node')

        self.obstacles_flottants = [Point() for _ in range(nb_drones+1)]
        self.obstacles_fixes    = []
        if mode==0:
            
            for obs in obstacles_data:
                obs_point=Point()
                obs_point.x=obs[0]
                obs_point.y=obs[1]
                obs_point.z=obs[2]
                self.obstacles_fixes.append(obs_point)

        # obs_point=Point()    #obstacle virtuel
        # obs_point.x=0.7
        # obs_point.y=0.5
        # obs_point.z=0.6
        # self.obstacles_fixes    = []

        self.recu_pos_w=False
        self.recu_pos_O=False
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.subscriptionW = self.create_subscription(PoseStamped,'/window/pose', self.poseW,qos)
        self.subscriptionO = self.create_subscription(PoseStamped,'/obstacle_1/pose', self.poseO1,qos)
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
        pos_point.z=0.5  #rayon de sécu du drone
        if i <= nb_drones :
            self.obstacles_flottants[i-1]=pos_point

    def send_info (self):
        obstacles          = PosObstacles()
        obstacles.fixes    = self.obstacles_fixes
        obstacles.flotants = self.obstacles_flottants
        self.publisher.publish(obstacles)
        
    def poseW (self,msg):
        if not(self.recu_pos_w):
            self.recu_pos_w=True
            obs_point1=Point()
            obs_point1.x=msg.pose.position.x+0.29  
            obs_point1.y=msg.pose.position.y           #,msg.pose.position.z
            obs_point1.z=0.10   #rayon
            obs_point2=Point()
            obs_point2.x=msg.pose.position.x-0.29 
            obs_point2.y=msg.pose.position.y            #,msg.pose.position.z
            obs_point2.z=0.10   #rayon
            self.obstacles_fixes.append(obs_point1)
            self.obstacles_fixes.append(obs_point2)
            #self.get_logger().info(f"_____________Position Window:({self.obstacles_fixes})")
        else:
            pass

    def poseO1 (self,msg):
        if not(self.recu_pos_O):
            self.recu_pos_O=True
            obs_point1=Point()
            obs_point1.x=msg.pose.position.x
            obs_point1.y=msg.pose.position.y           #,msg.pose.position.z
            obs_point1.z=0.45  #rayon
            self.obstacles_fixes.append(obs_point1)
            #self.get_logger().info(f"_____________Position obstacle1:({self.obstacles_fixes})")
        else:
            pass
        




def main(args=None):
    rclpy.init(args=args)
    node = fake_ot_node()  # Création du nœud
    rclpy.spin(node)  # Exécution du nœud
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()