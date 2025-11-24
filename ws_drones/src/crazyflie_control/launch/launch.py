from launch import LaunchDescription
from launch_ros.actions import Node
import json
# https://index.ros.org/r/vrpn_mocap/
config = {"crazyflie_1": "radio://3/10/2M/E7E7E70901",
          "crazyflie_2": "radio://0/20/2M/E7E7E70902",
          "crazyflie_3": "radio://1/30/2M/E7E7E70903",
          "crazyflie_5": "radio://2/50/2M/E7E7E70905"} #le 4 est bien bien bien loooong

# config = {"crazyflie_1": "radio://3/80/2M/E7E7E7E701",
#           "crazyflie_2": "radio://0/20/2M/E7E7E7E702",
#           "crazyflie_3": "radio://1/30/2M/E7E7E7E703",
#           "crazyflie_5": "radio://2/50/2M/E7E7E7E705"} 

all_radio = [[2],  # ch 20
             [3],  # ch 30
             [1],  # ch 80
             #[4],  # ch 40
             #[5], # ch 50
             ]







def generate_launch_description():
    node1 = Node(package='vrpn_mocap',
                 executable='client_node',
                #  parameters=[{"server": "192.168.2.10",
                #               "port": 3883}]
                 parameters=[{"server": "10.40.61.251", #251 à gauche / 252 à droite
                              "port": 3883}]
                              )
    nodes = [node1]
    for radio_id, cf_for_one_radio in enumerate(all_radio): 
        set_config = {}
        for i in cf_for_one_radio:
            cf_name = f"crazyflie_{i}"
            set_config[cf_name] = config[cf_name]

        node = Node(package='crazyflie_control',
                    executable='crazyflie_control_1',
                    name=f"crazyflie_control_{radio_id}",
                    arguments=[json.dumps(set_config)]
                    )
        nodes.append(node)    

    return LaunchDescription(nodes)