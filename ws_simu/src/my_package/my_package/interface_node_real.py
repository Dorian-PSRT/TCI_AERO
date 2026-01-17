#Node pour faire l'interface entre les positions d'OptiTrack et le reste des nodes
#Elle sert à transformer les positions envoyées par OptiTrack et les publiées sur les topic lus par les nodes
#note : ceci est une version optimisée de la version précédente par ChatGPT
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.qos import ReliabilityPolicy, QoSProfile
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import Imu
import math



class interface_node(Node):
    def __init__(self):
        super().__init__('interface_node')  
        self.cl_group = ReentrantCallbackGroup()

        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

        # === SUBSCRIPTIONS GPS ===
        self.create_subscription(PoseStamped, '/crazyflie_1/pose', lambda msg: self.cf1_gps_callback(msg, 1), qos, callback_group=self.cl_group)
        self.create_subscription(PoseStamped, '/crazyflie_2/pose', lambda msg: self.cf2_gps_callback(msg, 2), qos, callback_group=self.cl_group)
        self.create_subscription(PoseStamped, '/crazyflie_3/pose', lambda msg: self.cf3_gps_callback(msg, 3), qos, callback_group=self.cl_group)
        self.create_subscription(PoseStamped, '/crazyflie_4/pose', lambda msg: self.cf4_gps_callback(msg, 4), qos, callback_group=self.cl_group)

        # === POSE VERS TURTLESIM ===
        self.cf1_pose_pub = self.create_publisher(Pose, '/turtle1/pose', 10, callback_group=self.cl_group)
        self.cf2_pose_pub = self.create_publisher(Pose, '/turtle2/pose', 10, callback_group=self.cl_group)
        self.cf3_pose_pub = self.create_publisher(Pose, '/turtle3/pose', 10, callback_group=self.cl_group)
        self.cf4_pose_pub = self.create_publisher(Pose, '/turtle4/pose', 10, callback_group=self.cl_group)

        self.get_logger().info("Interface_node lancée.")
        # Stockage yaw
        self.yaw = [0.0] * 5  # index 1 à 4

    # === GPS + IDX ===
    def cf1_gps_callback(self, p_s, idx): self._publish_pose(p_s, self.cf1_pose_pub, idx)
    def cf2_gps_callback(self, p_s, idx): self._publish_pose(p_s, self.cf2_pose_pub, idx)
    def cf3_gps_callback(self, p_s, idx): self._publish_pose(p_s, self.cf3_pose_pub, idx)
    def cf4_gps_callback(self, p_s, idx): self._publish_pose(p_s, self.cf4_pose_pub, idx)

    # === IMU + IDX ===
    def cf1_imu_callback(self, msg, idx): self._update_yaw(msg, idx)
    def cf2_imu_callback(self, msg, idx): self._update_yaw(msg, idx)
    def cf3_imu_callback(self, msg, idx): self._update_yaw(msg, idx)
    def cf4_imu_callback(self, msg, idx): self._update_yaw(msg, idx)

    def _update_yaw(self, msg, idx):
        q = msg.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.yaw[idx] = math.atan2(siny_cosp, cosy_cosp)

    def _publish_pose(self, p_s, publisher, idx):
        pose = Pose()
        pose.x = p_s.pose.position.x
        pose.y = p_s.pose.position.y
        pose.theta = p_s.pose.position.z
        #pose.theta = self.yaw[idx]      # à méditer
        publisher.publish(pose)


def main(args=None):
    rclpy.init(args=args)
    node = interface_node()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
