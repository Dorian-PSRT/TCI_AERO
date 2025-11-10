import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PointStamped
import math


class SwarmController(Node):
    def __init__(self):
        super().__init__('swarm_controller')

        # Positions des deux drones
        self.cf1_pos = None
        self.cf2_pos = None

        # Souscriptions aux GPS
        self.create_subscription(PointStamped, '/Crazyflie1/gps', self.cf1_gps_callback, 10)
        self.create_subscription(PointStamped, '/Crazyflie2/gps', self.cf2_gps_callback, 10)

        # Publishers pour les commandes
        self.cf1_cmd_pub = self.create_publisher(Twist, '/Crazyflie1/cmd_vel', 10)
        self.cf2_cmd_pub = self.create_publisher(Twist, '/Crazyflie2/cmd_vel', 10)

        # Timer de contrôle
        self.timer = self.create_timer(0.2, self.control_loop)

        # Distances
        self.ideal_distance = 1.0   # distance cible (m)
        self.repulsion_gain = 0.5   # force de répulsion
        self.attraction_gain = 0.2  # force d’attraction

        self.get_logger().info("🧠 Swarm controller (champ de potentiel) initialisé.")

    def cf1_gps_callback(self, msg):
        self.cf1_pos = (msg.point.x, msg.point.y, msg.point.z)

    def cf2_gps_callback(self, msg):
        self.cf2_pos = (msg.point.x, msg.point.y, msg.point.z)

    def control_loop(self):
        if self.cf1_pos is None or self.cf2_pos is None:
            return

        dx = self.cf2_pos[0] - self.cf1_pos[0]
        dy = self.cf2_pos[1] - self.cf1_pos[1]
        distance = math.sqrt(dx**2 + dy**2)

        cmd1 = Twist()
        cmd2 = Twist()

        # Calcul de la force relative
        if distance < 0.01:
            return  # éviter les divisions par zéro

        direction_x = dx / distance
        direction_y = dy / distance

        # Force selon la distance
        if distance < self.ideal_distance:
            # Trop proche → s’éloignent
            force = self.repulsion_gain * (self.ideal_distance - distance)
            cmd1.linear.x = -force * direction_x
            cmd1.linear.y = -force * direction_y
            cmd2.linear.x = force * direction_x
            cmd2.linear.y = force * direction_y
        elif distance > self.ideal_distance * 1.5:
            # Trop loin → se rapprochent
            force = self.attraction_gain * (distance - self.ideal_distance)
            cmd1.linear.x = force * direction_x
            cmd1.linear.y = force * direction_y
            cmd2.linear.x = -force * direction_x
            cmd2.linear.y = -force * direction_y
        else:
            # Distance idéale → restent stables
            cmd1.linear.x = 0.0
            cmd1.linear.y = 0.0
            cmd2.linear.x = 0.0
            cmd2.linear.y = 0.0

        # Publier les vitesses
        self.cf1_cmd_pub.publish(cmd1)
        self.cf2_cmd_pub.publish(cmd2)

        self.get_logger().info(f"📡 Distance={distance:.2f} | cmd1=({cmd1.linear.x:.2f},{cmd1.linear.y:.2f})")


def main(args=None):
    rclpy.init(args=args)
    node = SwarmController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
