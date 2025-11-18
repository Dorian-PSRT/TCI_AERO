import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from geometry_msgs.msg import PoseStamped
from turtlesim.msg import Pose

import math


class InterfaceNode(Node):
    def __init__(self):
        super().__init__('interface_node')
        self.cl_group = ReentrantCallbackGroup()

        # ================================
        #   STORAGE FOR YAW (1..4 drones)
        # ================================
        self.yaw = [0.0] * 5

        # ============================================================
        #  PART 1 — /cfX/pose_d  →  /cfX/TargetPose   (setpoints)
        # ============================================================

        # -------- CF1 --------
        self.create_subscription(
            PoseStamped,
            '/crazyflie1/pose_d',
            self.cf1_pose_d_callback,
            10,
            callback_group=self.cl_group)
        self.cf1_target_pub = self.create_publisher(
            PoseStamped, '/crazyflie_1/TargetPose', 10)

        # -------- CF2 --------
        self.create_subscription(
            PoseStamped,
            '/crazyflie2/pose_d',
            self.cf2_pose_d_callback,
            10,
            callback_group=self.cl_group)
        self.cf2_target_pub = self.create_publisher(
            PoseStamped, '/crazyflie_2/TargetPose', 10)

        # -------- CF3 --------
        self.create_subscription(
            PoseStamped,
            '/crazyflie3/pose_d',
            self.cf3_pose_d_callback,
            10,
            callback_group=self.cl_group)
        self.cf3_target_pub = self.create_publisher(
            PoseStamped, '/crazyflie_3/TargetPose', 10)

        # -------- CF4 --------
        self.create_subscription(
            PoseStamped,
            '/crazyflie4/pose_d',
            self.cf4_pose_d_callback,
            10,
            callback_group=self.cl_group)
        self.cf4_target_pub = self.create_publisher(
            PoseStamped, '/crazyflie_4/TargetPose', 10)

        # ============================================================
        #  PART 2 — /cfX/pose  →  /turtleX/pose   (real position)
        # ============================================================

        # -------- CF1 --------
        self.create_subscription(
            PoseStamped,
            '/crazyflie_1/pose',
            lambda msg: self.cf1_pose_callback(msg, 1),
            10,
            callback_group=self.cl_group)
        self.cf1_pose_pub = self.create_publisher(Pose, '/turtle1/pose', 10)

        # -------- CF2 --------
        self.create_subscription(
            PoseStamped,
            '/crazyflie_2/pose',
            lambda msg: self.cf2_pose_callback(msg, 2),
            10,
            callback_group=self.cl_group)
        self.cf2_pose_pub = self.create_publisher(Pose, '/turtle2/pose', 10)

        # -------- CF3 --------
        self.create_subscription(
            PoseStamped,
            '/crazyflie_3/pose',
            lambda msg: self.cf3_pose_callback(msg, 3),
            10,
            callback_group=self.cl_group)
        self.cf3_pose_pub = self.create_publisher(Pose, '/turtle3/pose', 10)

        # -------- CF4 --------
        self.create_subscription(
            PoseStamped,
            '/crazyflie_4/pose',
            lambda msg: self.cf4_pose_callback(msg, 4),
            10,
            callback_group=self.cl_group)
        self.cf4_pose_pub = self.create_publisher(Pose, '/turtle4/pose', 10)

        self.get_logger().info("InterfaceNode READY: pose_d forwarding + real pose to turtlesim")


    # ====================================================
    #        PART 1 — FORWARD /cfX/pose_d → /cfX/TargetPose
    # ====================================================

    def cf1_pose_d_callback(self, msg): self.cf1_target_pub.publish(msg)
    def cf2_pose_d_callback(self, msg): self.cf2_target_pub.publish(msg)
    def cf3_pose_d_callback(self, msg): self.cf3_target_pub.publish(msg)
    def cf4_pose_d_callback(self, msg): self.cf4_target_pub.publish(msg)


    # ====================================================
    #        PART 2 — REAL CF POSE → turtlesim Pose
    # ====================================================

    def cf1_pose_callback(self, msg, idx): self._publish_turtle_pose(msg, self.cf1_pose_pub)
    def cf2_pose_callback(self, msg, idx): self._publish_turtle_pose(msg, self.cf2_pose_pub)
    def cf3_pose_callback(self, msg, idx): self._publish_turtle_pose(msg, self.cf3_pose_pub)
    def cf4_pose_callback(self, msg, idx): self._publish_turtle_pose(msg, self.cf4_pose_pub)

    def _publish_turtle_pose(self, msg, publisher):
        pose = Pose()

        # XY from PoseStamped
        pose.x = msg.pose.position.x
        pose.y = msg.pose.position.y

        # Convert quaternion → yaw (theta for turtlesim)
        q = msg.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y*q.y + q.z*q.z)
        pose.theta = math.atan2(siny_cosp, cosy_cosp)

        publisher.publish(pose)


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()
    node = InterfaceNode()
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
