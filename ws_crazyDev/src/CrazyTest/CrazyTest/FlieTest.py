import rclpy 
from rclpy.node import Node 
import cflib.crtp
from cflib.crazyflie import Crazyflie
from rclpy.executors import MultiThreadedExecutor


class SimpleNode1(Node):
    def __init__(self):
        super().__init__('simple_node1')  # Nom du nœud
        # Initialiser les drivers (nécessaire pour que Crazyradio fonctionne)
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()
        for i in available:
            print("Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1]))


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()
    node = SimpleNode1()  # Création du nœud
    executor.add_node(node)
    #rclpy.spin(node)  # Exécution du nœud
    executor.spin()
    
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()