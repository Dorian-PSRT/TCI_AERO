import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import Point
from std_msgs.msg import Bool


class observer_Node(Node):                        
    def __init__(self):
        super().__init__(f'Observer_Node')  # Nom du nœud        

        self.cl_group = ReentrantCallbackGroup()

        self.subscription1 = self.create_subscription(Point,'/turtle1/bestTurtle' ,self.tor1,10, callback_group= self.cl_group) 
        self.subscription2 = self.create_subscription(Point,'/turtle2/bestTurtle' ,self.tor2,10, callback_group= self.cl_group)  
        self.subscription3 = self.create_subscription(Point,'/turtle3/bestTurtle' ,self.tor3,10, callback_group= self.cl_group)
        self.subscription4 = self.create_subscription(Point,'/turtle4/bestTurtle' ,self.tor4,10, callback_group= self.cl_group) 
        self.go_1 = self.create_subscription(Bool,'/turtle1/go' ,self.go1,10, callback_group= self.cl_group) 
        self.go_2 = self.create_subscription(Bool,'/turtle2/go' ,self.go2,10, callback_group= self.cl_group) 
        self.go_3 = self.create_subscription(Bool,'/turtle3/go' ,self.go3,10, callback_group= self.cl_group) 
        self.go_4 = self.create_subscription(Bool,'/turtle4/go' ,self.go4,10, callback_group= self.cl_group) 


    def tor1(self,msg):
        self.get_logger().info(f"Tor1 : msg reçu :{msg}")

    def tor2(self,msg):
        self.get_logger().info(f"Tor2 : msg reçu :{msg}")

    def tor3(self,msg):
        self.get_logger().info(f"Tor3 : msg reçu :{msg}")

    def tor4(self,msg):
        self.get_logger().info(f"Tor4 : msg reçu :{msg}")

    def go1(self,msg):
        self.get_logger().info(f"Tor1 : GO reçu :{msg}")
    def go2(self,msg):
        self.get_logger().info(f"Tor2 : GO reçu :{msg}")
    def go3(self,msg):
        self.get_logger().info(f"Tor3 : GO reçu :{msg}")
    def go4(self,msg):
        self.get_logger().info(f"Tor4 : GO reçu :{msg}")


def main(args=None):
    rclpy.init(args=args)
    node = observer_Node()  # Création du nœud                     
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    #rclpy.spin(node)  # Exécution du nœud
    executor.spin()
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()