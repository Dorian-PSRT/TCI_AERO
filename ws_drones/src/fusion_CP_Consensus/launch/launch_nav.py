from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='fusion_CP_Consensus',
            executable='local_path_node1',
            name='local_path_1'
        ),
        Node(
            package='fusion_CP_Consensus',
            executable='global_path_node1',
            name='global_path_1'
        ),
        Node(
            package='fusion_CP_Consensus',
            executable='decision_node1',
            name='MaxConsensus_1'
        )
        
    ])