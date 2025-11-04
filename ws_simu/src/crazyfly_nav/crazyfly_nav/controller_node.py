import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped

class CrazyflyController(Node):
    """
    Ce node contrôle un drone Crazyflie dans Webots via ROS 2.
    Il publie sur /cmd_vel pour déplacer le drone,
    et s'abonne à /odom pour recevoir sa position.
    """

    def __init__(self):
        super().__init__('crazyfly_controller')

        # 🟢 Publisher pour envoyer les vitesses au drone
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # 🟡 Subscriber pour écouter la position (odométrie)
        self.gps_sub = self.create_subscription(
        PointStamped,
        '/Crazyflie/gps',
        self.gps_callback,
        10
             )

        # 🔵 Timer pour exécuter une boucle de contrôle à 10 Hz
        self.timer = self.create_timer(0.1, self.control_loop)

        # Stocker la dernière pose connue
        self.pose = None

        self.get_logger().info('✅ Crazyfly controller node initialized.')

    # ------------------------------------------------------------------
    def gps_callback(self, msg):
        x = msg.point.x
        y = msg.point.y
        z = msg.point.z
        self.get_logger().info(f"📡 GPS reçu : x={x:.2f}, y={y:.2f}, z={z:.2f}")
        self.pose = (x, y, z)


    # ------------------------------------------------------------------
    def control_loop(self):
        """Boucle de commande appelée périodiquement (toutes les 0.1 s)."""
        if self.pose is None:
            self.get_logger().info("❌ Pose non reçue ")
            return

        # Créer un message Twist pour avancer lentement vers l'avant
        cmd = Twist()
        cmd.linear.x = 0.2  # avance doucement
        cmd.linear.z = 0.0  # pas de montée
        cmd.angular.z = 0.0  # pas de rotation
        self.cmd_pub.publish(cmd)

        self.get_logger().info('🚁 Drone avance doucement.')

# ----------------------------------------------------------------------

def main(args=None):
    """Point d'entrée du programme."""
    rclpy.init(args=args)
    node = CrazyflyController()
    try:
        rclpy.spin(node)  # exécute la boucle ROS 2
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
