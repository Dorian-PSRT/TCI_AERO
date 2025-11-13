#  ...........       ____  _ __
#  |  ,-^-,  |      / __ )(_) /_______________ _____  ___
#  | (  O  ) |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  | / ,..´  |    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#     +.......   /_____/_/\__/\___/_/   \__,_/ /___/\___/

# MIT License

# Copyright (c) 2023 Bitcraze

# @file crazyflie_driver.py
# Controls the crazyflie motors in Webots using ROS2.

"""crazyflie_driver"""


import math
import rclpy
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan, Imu
import numpy as np
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Float32 
from tf2_ros import TransformBroadcaster
import tf_transformations
from turtlesim.msg import Pose

from math import cos, sin
from my_package.pid_vel import QuadrotorController

FLYING_ATTITUDE = 1


#class Transfo:
#    def __init__(self):

#        self.gps = self.robot.getDevice("gps")
#        self.publisher = self.create_publisher(Pose, f'/{self.robot.getName()}/pose', 10)
    
#    def transformation_step(self):

#        self.pose.x = self.gps.getValues()[0]
#        self.pose.y = self.gps.getValues()[1]
     




class CrazyflieDriver:

    def init(self, webots_node, properties):

        self.robot = webots_node.robot
        self.timestep = int(self.robot.getBasicTimeStep())

        # Initialize motors
        self.m1_motor = self.robot.getDevice("m1_motor")
        self.m1_motor.setPosition(float('inf'))
        self.m1_motor.setVelocity(-1)
        self.m2_motor = self.robot.getDevice("m2_motor")
        self.m2_motor.setPosition(float('inf'))
        self.m2_motor.setVelocity(1)
        self.m3_motor = self.robot.getDevice("m3_motor")
        self.m3_motor.setPosition(float('inf'))
        self.m3_motor.setVelocity(-1)
        self.m4_motor = self.robot.getDevice("m4_motor")
        self.m4_motor.setPosition(float('inf'))
        self.m4_motor.setVelocity(1)

        # Initialize Sensors
        self.imu = self.robot.getDevice("inertial_unit")
        self.imu.enable(self.timestep)
        self.gps = self.robot.getDevice("gps")
        self.gps.enable(self.timestep)
        self.gyro = self.robot.getDevice("gyro")
        self.gyro.enable(self.timestep)
        self.camera = self.robot.getDevice("camera")
        self.camera.enable(self.timestep)
        self.range_front = self.robot.getDevice("range_front")
        self.range_front.enable(self.timestep)
        self.range_left = self.robot.getDevice("range_left")
        self.range_left.enable(self.timestep)
        self.range_back = self.robot.getDevice("range_back")
        self.range_back.enable(self.timestep)
        self.range_right = self.robot.getDevice("range_right")
        self.range_right.enable(self.timestep)

        # Initialize variables
        self.past_x_global = 0
        self.past_y_global = 0
        self.past_time = self.robot.getTime()

        # Crazyflie velocity PID controller
        self.PID_CF = pid_velocity_fixed_height_controller()
        self.PID_update_last_time = self.robot.getTime()
        self.sensor_read_last_time = self.robot.getTime()

        self.vel_cmd_twist = Twist()
        self.height_desired = FLYING_ATTITUDE

        # === Contrôleur de position (utilise PID_vel.py tel quel) ===
        self.position_controller = QuadrotorController()
        self.target_position = [0.0, 0.0, FLYING_ATTITUDE, 0.0, 0.0, 0.0]  # x, y, z, roll, pitch, yaw
        self.use_position_control = False

                    # États internes pour navigation
        global buscando_direccion, personaDetectada, crearRecorrido
        buscando_direccion = True
        personaDetectada = False
        crearRecorrido = False


        # Intialize ROS
        rclpy.init(args=None)
        self.node = rclpy.create_node('crazyflie_driver')

        # Topic pour recevoir une position cible
        self.node.create_subscription(
            PoseStamped, f"/{self.robot.getName()}/cmd_pos", self.cmd_pos_callback, 1
        )
        
        self.node.create_subscription(
            Twist, f"/{self.robot.getName()}/cmd_vel", self.cmd_vel_callback, 1)
        self.laser_publisher = self.node.create_publisher(
            LaserScan, f"/{self.robot.getName()}/scan", 1)
        self.imu_publisher = self.node.create_publisher(
            Imu, f"/{self.robot.getName()}/imu", 1)
        self.yaw_publisher = self.node.create_publisher(
            Float32, f"/{self.robot.getName()}/yaw", 10)
        self.static_broadcaster = TransformBroadcaster(self.node)
        self.first_time = True





    def cmd_vel_callback(self, twist):
        self.vel_cmd_twist = twist

    def cmd_pos_callback(self, msg):
        x = msg.pose.position.x
        y = msg.pose.position.y
        z = msg.pose.position.z

        # Optionnel : extraire yaw du quaternion
        q = [msg.pose.orientation.x, msg.pose.orientation.y,
            msg.pose.orientation.z, msg.pose.orientation.w]
        yaw = tf_transformations.euler_from_quaternion(q)[2]

        self.target_position = [x, y, z, 0.0, 0.0, yaw]  # roll/pitch = 0
        self.use_position_control = True
        self.node.get_logger().info(f"Cible position reçue : ({x:.2f}, {y:.2f}, {z:.2f})")

    def navigate_to_target(self, current_position, target_position, dt):

        global buscando_direccion  # état de rotation
        global crearRecorrido
        global personaDetectada
        global t_detectada
        global total_simulation_time
        global t_espera_persona

        # === Décomposition ===
        x, y, z, roll, pitch, yaw = current_position
        yaw_desired = 0.0
        forward_desired = 0.0
        sideways_desired = 0.0
        height_diff_desired = 0.0

        # --- Angle vers la cible ---
        alpha = math.atan2((target_position[1] - y), (target_position[0]) - x)

        # === Phase orientation ===
        if buscando_direccion:
            if yaw >= math.pi/2 and yaw * alpha < 0:
                current_position_desplazada = yaw - math.pi
                alpha_desplazada = alpha - math.pi/2
                if current_position_desplazada > alpha_desplazada + 0.1:
                    yaw_desired = +0.15
                elif current_position_desplazada < alpha_desplazada - 0.1:
                    yaw_desired = -0.15
            elif yaw <= -math.pi/2 and yaw * alpha < 0:
                current_position_desplazada = yaw - math.pi
                alpha_desplazada = alpha - math.pi/2
                if current_position_desplazada > alpha_desplazada + 0.1:
                    yaw_desired = +0.15
                elif current_position_desplazada < alpha_desplazada - 0.1:
                    yaw_desired = -0.15
            else:
                if yaw > alpha + 0.1:
                    yaw_desired = -0.15
                elif yaw < alpha - 0.1:
                    yaw_desired = +0.15
                else:
                    buscando_direccion = False

        # === Phase déplacement ===
        else:
            buscando_direccion = False
            if personaDetectada:
                t_espera_persona = total_simulation_time - t_detectada
                forward_desired = 0
                sideways_desired = 0
                yaw_desired = 0
                height_diff_desired = 0
                self.node.get_logger().info("🧍 Persona detectada — arrêt du drone")
            else:
                # PID de position
                cmd_vel_x, cmd_vel_y, cmd_ang_w = self.position_controller.control_quadrotor(
                    current_position, target_position, dt
                )
                if target_position[2] > z:
                    height_diff_desired = min(target_position[2] - z, 0.1)
                if target_position[2] < z:
                    height_diff_desired = max(target_position[2] - z, -0.1)
                
                sideways_desired = cmd_vel_y
                forward_desired = cmd_vel_x
                yaw_desired = cmd_ang_w

                # Distances à la cible
                distTargetX = abs(target_position[0] - x)
                distTargetY = abs(target_position[1] - y)
                distTargetZ = abs(target_position[2] - z)

                # Même logique que ton code original
                if distTargetX < 0.2 and distTargetY < 0.2 and distTargetZ < 0.3:
                    buscando_direccion = True
                    self.node.get_logger().info("✅ Cible atteinte !")
                    self.use_position_control = False  # stop mode autonome

        return forward_desired, sideways_desired, yaw_desired, height_diff_desired


    def step(self):

        rclpy.spin_once(self.node, timeout_sec=0)
        dt = self.robot.getTime() - self.past_time

        if self.first_time:
            self.past_x_global = self.gps.getValues()[0]
            self.past_y_global = self.gps.getValues()[1]
            self.past_time = self.robot.getTime()
            self.first_time = False
        else:
            dt = self.robot.getTime() - self.past_time

        # Get sensor data
        roll = self.imu.getRollPitchYaw()[0]
        pitch = -self.imu.getRollPitchYaw()[1]
        yaw = self.imu.getRollPitchYaw()[2]
        yaw_rate = self.gyro.getValues()[2]
        altitude = self.gps.getValues()[2]
        x_global = self.gps.getValues()[0]
        v_x_global = (x_global - self.past_x_global)/dt
        y_global = self.gps.getValues()[1]
        v_y_global = (y_global - self.past_y_global)/dt
        z_global = self.gps.getValues()[2]


        # Get body fixed velocities
        cosyaw = cos(yaw)
        sinyaw = sin(yaw)
        v_x = v_x_global * cosyaw + v_y_global * sinyaw
        v_y = - v_x_global * sinyaw + v_y_global * cosyaw

        # # === Position step ===
        # if self.use_position_control:
        #     current_pos = [
        #         x_global, y_global, z_global,
        #         roll, pitch, yaw
        #     ]
        #     forward_desired, sideways_desired, yaw_desired = self.position_controller.control_quadrotor(
        #         current_pos, self.target_position, dt
        #     )
        #     height_diff_desired = 0.0  # z géré par le PID de vitesse existant
        #     self.height_desired = self.target_position[2]  # z cible
        # === Position step ===
        if self.use_position_control:
            current_pos = [x_global, y_global, z_global, roll, pitch, yaw]
            forward_desired, sideways_desired, yaw_desired, height_diff_desired = \
                self.navigate_to_target(current_pos, self.target_position, dt)
            self.height_desired += height_diff_desired * dt
        else:
            forward_desired = self.vel_cmd_twist.linear.x
            sideways_desired = self.vel_cmd_twist.linear.y
            yaw_desired = self.vel_cmd_twist.angular.z
            height_diff_desired = self.vel_cmd_twist.linear.z
            self.height_desired += height_diff_desired * dt

        # Example how to get sensor data
        ranges = [self.range_back.getValue()/1000.0, self.range_left.getValue()/1000.0,
                  self.range_front.getValue()/1000.0, self.range_right.getValue()/1000.0]


        # === PUBLIE LE YAW EN CLAIR (FLOAT32) ===
        yaw_msg = Float32()
        yaw_msg.data = yaw  # yaw = self.imu.getRollPitchYaw()[2] → déjà calculé !
        self.yaw_publisher.publish(yaw_msg)

         # 1. Créer le message Imu
        imu_msg = Imu()
        imu_msg.header.stamp = self.node.get_clock().now().to_msg()
        imu_msg.header.frame_id = self.robot.getName() # ex: "Crazyflie1"

        # 2. Remplir l'orientation (en quaternion)
        # Le code le calcule déjà pour TF, on peut le réutiliser
        q = tf_transformations.quaternion_from_euler(roll, pitch, yaw)
        imu_msg.orientation.x = q[0]
        imu_msg.orientation.y = q[1]
        imu_msg.orientation.z = q[2]
        imu_msg.orientation.w = q[3]

        # 3. Remplir la vitesse angulaire (depuis le gyroscope)
        gyro_values = self.gyro.getValues()
        imu_msg.angular_velocity.x = gyro_values[0]
        imu_msg.angular_velocity.y = gyro_values[1]
        imu_msg.angular_velocity.z = gyro_values[2]

        # 4. Remplir l'accélération linéaire
        # Note: l'IMU de Webots ne fournit pas directement l'accélération.
        # On la laisse à zéro, ce qui est une pratique courante
        # lorsque le capteur ne fournit pas cette donnée.
        imu_msg.linear_acceleration.x = 0.0
        imu_msg.linear_acceleration.y = 0.0
        imu_msg.linear_acceleration.z = 0.0
        
        # 5. Publier le message !
        self.imu_publisher.publish(imu_msg)
        # ==========================================================

        # Publish laser scan
        scan_msg = LaserScan()
        scan_msg.header.stamp = self.node.get_clock().now().to_msg()
        scan_msg.header.frame_id = 'crazyflie'
        scan_msg.angle_min = -0.5 * 2 * math.pi
        scan_msg.angle_max = 0.25 * 2 * math.pi
        scan_msg.angle_increment = 1.0 * math.pi/2
        scan_msg.range_min = 0.1
        scan_msg.range_max = 2.0
        scan_msg.ranges = ranges
        self.laser_publisher.publish(scan_msg)

        # Publish static transform
        laser_transform = TransformStamped()
        q = tf_transformations.quaternion_from_euler(roll, pitch, yaw)
        laser_transform = TransformStamped()
        laser_transform.header.stamp = self.node.get_clock().now().to_msg()
        laser_transform.header.frame_id = 'odom'
        laser_transform.child_frame_id =   self.robot.getName() #'crazyflie'
        laser_transform.transform.translation.x = x_global
        laser_transform.transform.translation.y = y_global
        laser_transform.transform.translation.z = z_global
        laser_transform.transform.rotation.x = q[0]
        laser_transform.transform.rotation.y = q[1]
        laser_transform.transform.rotation.z = q[2]
        laser_transform.transform.rotation.w = q[3]

        self.static_broadcaster.sendTransform(laser_transform)

        # PID velocity controller with fixed height
        motor_power = self.PID_CF.pid(dt, forward_desired, sideways_desired,
                                      yaw_desired, self.height_desired,
                                      roll, pitch, yaw_rate,
                                      altitude, v_x, v_y)

        self.m1_motor.setVelocity(-motor_power[0])
        self.m2_motor.setVelocity(motor_power[1])
        self.m3_motor.setVelocity(-motor_power[2])
        self.m4_motor.setVelocity(motor_power[3])

        self.past_time = self.robot.getTime()
        self.past_x_global = x_global
        self.past_y_global = y_global


class pid_velocity_fixed_height_controller():
    def __init__(self):
        self.past_vx_error = 0.0
        self.past_vy_error = 0.0
        self.past_alt_error = 0.0
        self.past_pitch_error = 0.0
        self.past_roll_error = 0.0
        self.altitude_integrator = 0.0
        self.last_time = 0.0

    def pid(self, dt, desired_vx, desired_vy, desired_yaw_rate, desired_altitude, actual_roll, actual_pitch, actual_yaw_rate,
            actual_altitude, actual_vx, actual_vy):
        # Velocity PID control (converted from Crazyflie c code)
        gains = {"kp_att_y": 1, "kd_att_y": 0.5, "kp_att_rp": 0.5, "kd_att_rp": 0.1,
                 "kp_vel_xy": 2, "kd_vel_xy": 0.5, "kp_z": 10, "ki_z": 5, "kd_z": 5}

        # Velocity PID control
        vx_error = desired_vx - actual_vx
        vx_deriv = (vx_error - self.past_vx_error) / dt
        vy_error = desired_vy - actual_vy
        vy_deriv = (vy_error - self.past_vy_error) / dt
        desired_pitch = gains["kp_vel_xy"] * \
            np.clip(vx_error, -1, 1) + gains["kd_vel_xy"] * vx_deriv
        desired_roll = -gains["kp_vel_xy"] * \
            np.clip(vy_error, -1, 1) - gains["kd_vel_xy"] * vy_deriv
        self.past_vx_error = vx_error
        self.past_vy_error = vy_error

        # Altitude PID control
        alt_error = desired_altitude - actual_altitude
        alt_deriv = (alt_error - self.past_alt_error) / dt
        self.altitude_integrator += alt_error * dt
        alt_command = gains["kp_z"] * alt_error + gains["kd_z"] * alt_deriv + \
            gains["ki_z"] * np.clip(self.altitude_integrator, -2, 2) + 48
        self.past_alt_error = alt_error

        # Attitude PID control
        pitch_error = desired_pitch - actual_pitch
        pitch_deriv = (pitch_error - self.past_pitch_error) / dt
        roll_error = desired_roll - actual_roll
        roll_deriv = (roll_error - self.past_roll_error) / dt
        yaw_rate_error = desired_yaw_rate - actual_yaw_rate
        roll_command = gains["kp_att_rp"] * \
            np.clip(roll_error, -1, 1) + gains["kd_att_rp"] * roll_deriv
        pitch_command = -gains["kp_att_rp"] * \
            np.clip(pitch_error, -1, 1) - gains["kd_att_rp"] * pitch_deriv
        yaw_command = gains["kp_att_y"] * np.clip(yaw_rate_error, -1, 1)
        self.past_pitch_error = pitch_error
        self.past_roll_error = roll_error

        # Motor mixing
        m1 = alt_command - roll_command + pitch_command + yaw_command
        m2 = alt_command - roll_command - pitch_command - yaw_command
        m3 = alt_command + roll_command - pitch_command + yaw_command
        m4 = alt_command + roll_command + pitch_command - yaw_command

        # Limit the motor command
        m1 = np.clip(m1, 0, 600)
        m2 = np.clip(m2, 0, 600)
        m3 = np.clip(m3, 0, 600)
        m4 = np.clip(m4, 0, 600)

        return [m1, m2, m3, m4]


