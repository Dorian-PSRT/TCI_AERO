from setuptools import find_packages, setup
import glob

package_name = 'crazyflie_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/launch.py', 'launch/takeoff.launch.py']  ),
        ('share/' + package_name + '/config', ['config/params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='estacalab',
    maintainer_email='estacalab@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'crazyflie_control_1= crazyflie_control.crazyflie_control_node:main',
            'takeoff_client= crazyflie_control.takeoff_client:main',
            
        ],
    },
)
