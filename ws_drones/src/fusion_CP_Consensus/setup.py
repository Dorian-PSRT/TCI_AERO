from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'fusion_CP_Consensus'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='etu.tci',
    maintainer_email='etu.tci@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
    'my_robot_driver_node4 = fusion_CP_Consensus.my_robot_driver_node4:main',
    'my_robot_driver_node3 = fusion_CP_Consensus.my_robot_driver_node3:main',
    'my_robot_driver_node2 = fusion_CP_Consensus.my_robot_driver_node2:main',
    'my_robot_driver_node1 = fusion_CP_Consensus.my_robot_driver_node1:main',
    'local_path_node4 = fusion_CP_Consensus.local_path_node4:main',
    'local_path_node3 = fusion_CP_Consensus.local_path_node3:main',
    'local_path_node2 = fusion_CP_Consensus.local_path_node2:main',
    'local_path_node1 = fusion_CP_Consensus.local_path_node1:main',
    'global_path_node4 = fusion_CP_Consensus.global_path_node4:main',
    'global_path_node3 = fusion_CP_Consensus.global_path_node3:main',
    'global_path_node2 = fusion_CP_Consensus.global_path_node2:main',
    'global_path_node1 = fusion_CP_Consensus.global_path_node1:main',
    'fake_ot_node = fusion_CP_Consensus.fake_ot_node:main',
    'decision_node4 = fusion_CP_Consensus.decision_node4:main',
    'decision_node3 = fusion_CP_Consensus.decision_node3:main',
    'decision_node2 = fusion_CP_Consensus.decision_node2:main',
    'decision_node1 = fusion_CP_Consensus.decision_node1:main',
],
    },
)
