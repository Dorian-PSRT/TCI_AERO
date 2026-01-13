from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'tortues'

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
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'Turtle1_Node = tortues.Turtle1_Node:main',       #modifier
            'Turtle2_Node = tortues.Turtle2_Node:main',
            'Turtle3_Node = tortues.Turtle3_Node:main',
            'Turtle4_Node = tortues.Turtle4_Node:main',
            'spawn = tortues.testSTART:main',
            'observer = tortues.observer:main',
        ],
    },
)
