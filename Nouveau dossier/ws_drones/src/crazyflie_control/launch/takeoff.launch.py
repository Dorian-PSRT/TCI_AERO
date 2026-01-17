from launch import LaunchDescription
from launch_ros.actions import Node
# https://index.ros.org/r/vrpn_mocap/



crazyflie_list = [2, 3, 1, 5]

def generate_launch_description():
    nodes = []
    for i in crazyflie_list:
        cf_name = f"crazyflie_{i}"
        node = Node(
            package='crazyflie_control',  # package où se trouve takeoff_client.py
            executable='takeoff_client',
            name=f"{cf_name}_takeoff_client",
            namespace=cf_name,
            arguments=[cf_name]
        )
        nodes.append(node)

    return LaunchDescription(nodes)
