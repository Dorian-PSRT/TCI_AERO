import motioncapture
import rclpy 

from geometry_msgs.msg import Pose
from rclpy.node import Node 


mocap_system_type = 'optitrack'
host_name = '192.168.2.10'

class MocapNode(Node):
    def __init__(self):
        super().__init__('mocap_node')

        self.list_topic = {}

        self.mc = motioncapture.connect(mocap_system_type, {'hostname': host_name})
        self.timer = self.create_timer(0.01, self.mocap_callback)

    def mocap_callback(self):
        self.mc.waitForNextFrame()
        for name, obj in self.mc.rigidBodies.items():
            if 'crazyflie' in name:    
                topic_name = f"/{name}/pose"
                
                print(self.list_topic)

                if self.list_topic.get(topic_name):
                    pos = obj.position
                    rot = obj.rotation
                    pose = Pose()
                    pose.position.x = float(pos[0])
                    pose.position.y = float(pos[1])
                    pose.position.z = float(pos[2])
                    pose.orientation.x = float(rot.x)
                    pose.orientation.y = float(rot.y)
                    pose.orientation.z = float(rot.z)
                    pose.orientation.w = float(rot.w)
                    self.list_topic[topic_name].publish(pose)                    
                else:
                    self.list_topic[topic_name] = self.create_publisher(Pose, topic_name, 10)

def main(args=None):
    rclpy.init(args=args)
    node = MocapNode()  # Création du nœud
    rclpy.spin(node)  # Exécution du nœud
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()