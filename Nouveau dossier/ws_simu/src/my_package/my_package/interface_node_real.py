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

        # # === SUBSCRIPTIONS IMU (minuscule !) ===
        # self.create_subscription(Imu, '/Crazyflie1/imu', lambda msg: self.cf1_imu_callback(msg, 1), 10, callback_group=self.cl_group)
        # self.create_subscription(Imu, '/Crazyflie2/imu', lambda msg: self.cf2_imu_callback(msg, 2), 10, callback_group=self.cl_group)
        # self.create_subscription(Imu, '/Crazyflie3/imu', lambda msg: self.cf3_imu_callback(msg, 3), 10, callback_group=self.cl_group)
        # self.create_subscription(Imu, '/Crazyflie4/imu', lambda msg: self.cf4_imu_callback(msg, 4), 10, callback_group=self.cl_group)

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






# import rclpy
# from rclpy.node import Node
# from rclpy.executors import MultiThreadedExecutor
# from rclpy.callback_groups import ReentrantCallbackGroup
# from turtlesim.msg import Pose
# from geometry_msgs.msg import Twist, PointStamped


# from time import sleep
  

# class interface_node(Node):                                   #modifier
#     def __init__(self):
#         super().__init__(f'interface_node')  # Nom du nœud          #modifier

#         self.cl_group = ReentrantCallbackGroup()

#         #côté simu
#         self.cf1_cmd_pub = self.create_publisher(Twist, '/Crazyflie1/cmd_vel', 10, callback_group=self.cl_group)
#         self.cf2_cmd_pub = self.create_publisher(Twist, '/Crazyflie2/cmd_vel', 10, callback_group=self.cl_group)
#         self.cf3_cmd_pub = self.create_publisher(Twist, '/Crazyflie3/cmd_vel', 10, callback_group=self.cl_group)
#         self.cf4_cmd_pub = self.create_publisher(Twist, '/Crazyflie4/cmd_vel', 10, callback_group=self.cl_group)

#         self.create_subscription(PointStamped, '/Crazyflie1/gps', self.cf1_gps_callback, 10, callback_group=self.cl_group)
#         self.create_subscription(PointStamped, '/Crazyflie2/gps', self.cf2_gps_callback, 10, callback_group=self.cl_group)
#         self.create_subscription(PointStamped, '/Crazyflie3/gps', self.cf3_gps_callback, 10, callback_group=self.cl_group)
#         self.create_subscription(PointStamped, '/Crazyflie4/gps', self.cf4_gps_callback, 10, callback_group=self.cl_group)

#         #côté turtlesim
#         self.cf1_pose_pub = self.create_publisher(Pose, '/turtle1/pose', 10, callback_group=self.cl_group)
#         self.cf2_pose_pub = self.create_publisher(Pose, '/turtle2/pose', 10, callback_group=self.cl_group)
#         self.cf3_pose_pub = self.create_publisher(Pose, '/turtle3/pose', 10, callback_group=self.cl_group)
#         self.cf4_pose_pub = self.create_publisher(Pose, '/turtle4/pose', 10, callback_group=self.cl_group)

#         self.create_subscription(Twist, '/turtle1/cmd_vel', self.cf1_cmd_vel_callback, 10, callback_group=self.cl_group)
#         self.create_subscription(Twist, '/turtle2/cmd_vel', self.cf2_cmd_vel_callback, 10, callback_group=self.cl_group)
#         self.create_subscription(Twist, '/turtle3/cmd_vel', self.cf3_cmd_vel_callback, 10, callback_group=self.cl_group)
#         self.create_subscription(Twist, '/turtle4/cmd_vel', self.cf4_cmd_vel_callback, 10, callback_group=self.cl_group)

#     def cf1_gps_callback (self,p_s):
#         pose=Pose()
#         pose.x,pose.y = p_s.point.x,p_s.point.y
#         self.cf1_pose_pub.publish(pose)

#     def cf2_gps_callback (self,p_s):
#         pose=Pose()
#         pose.x,pose.y = p_s.point.x,p_s.point.y
#         self.cf2_pose_pub.publish(pose)

#     def cf3_gps_callback (self,p_s):
#         pose=Pose()
#         pose.x,pose.y = p_s.point.x,p_s.point.y
#         self.cf3_pose_pub.publish(pose)

#     def cf4_gps_callback (self,p_s):
#         pose=Pose()
#         pose.x,pose.y = p_s.point.x,p_s.point.y
#         self.cf4_pose_pub.publish(pose)

#     def cf1_cmd_vel_callback(self,cmd):
#         self.cf1_cmd_pub.publish(cmd)

#     def cf2_cmd_vel_callback(self,cmd):
#         self.cf2_cmd_pub.publish(cmd)

#     def cf3_cmd_vel_callback(self,cmd):
#         self.cf3_cmd_pub.publish(cmd)

#     def cf4_cmd_vel_callback(self,cmd):
#         self.cf4_cmd_pub.publish(cmd)

# def main(args=None):
#     rclpy.init(args=args)
#     node = interface_node()  # Création du nœud                      #modifier
#     executor = MultiThreadedExecutor()
#     executor.add_node(node)
#     #rclpy.spin(node)  # Exécution du nœud
#     executor.spin()
#     node.destroy_node()  # Destruction du nœud lors de l'arrêt
#     rclpy.shutdown()  # Arrêt de ROS2

# if __name__ == '__main__':
#     main()