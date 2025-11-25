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
    'local_path_node1 = fusion_CP_Consensus.local_path_node1:main',
    'global_path_node1 = fusion_CP_Consensus.global_path_node1:main',
    'fake_ot_node = fusion_CP_Consensus.fake_ot_node:main',
    'decision_node1 = fusion_CP_Consensus.decision_node1:main',
],
    },
)
