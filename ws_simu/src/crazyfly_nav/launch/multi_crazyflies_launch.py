import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    webots_pkg = get_package_share_directory('webots_ros2_crazyflie')

    return LaunchDescription([
        # Drone 1 : Crazyflie1
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(webots_pkg, 'launch', 'robot_launch.py')
            ),
            launch_arguments={
                'world': 'crazyflie_apartment.wbt',
                'namespace': 'crazyflie1'
            }.items()
        ),

        # Drone 2 : Crazyflie2
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(webots_pkg, 'launch', 'robot_launch.py')
            ),
            launch_arguments={
                'world': 'crazyflie_apartment.wbt',
                'namespace': 'crazyflie2'
            }.items()
        ),
    ])
