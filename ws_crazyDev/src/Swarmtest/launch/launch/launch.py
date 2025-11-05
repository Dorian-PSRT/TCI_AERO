import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

package_name = 'crazyflie_test'

def generate_launch_description():

    crazyflies_yaml_path = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'crazyflies.yaml')
    motion_capture_yaml_path = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'motion_capture.yaml')

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [
                        os.path.join(
                            get_package_share_directory('crazyflie'), 'launch'
                        ),
                        '/launch.py',
                    ]
                ),
                launch_arguments={
                    'crazyflies_yaml_file': crazyflies_yaml_path,
                    'motion_capture_yaml_file': motion_capture_yaml_path,
                }.items(),
            ),
        ]
    )
