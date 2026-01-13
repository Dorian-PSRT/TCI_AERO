import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController

name =['Crazyflie1','Crazyflie2','Crazyflie3','Crazyflie4']
contoller=[]

def generate_launch_description():
    package_dir = get_package_share_directory('my_package')
    robot_description_path = os.path.join(package_dir, 'resource', 'my_robot.urdf')

    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'my_world.wbt')
    )
    for i in name:
        my_robot_driver = WebotsController(
            robot_name=i,
            parameters=[
                {'robot_description': robot_description_path},
            ],
            respawn=True
        )
        contoller.append(my_robot_driver)

    return LaunchDescription([
        webots,
        *contoller,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])


