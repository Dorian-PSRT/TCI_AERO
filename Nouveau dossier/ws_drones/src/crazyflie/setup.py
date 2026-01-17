from setuptools import find_packages, setup

package_name = 'crazyflie'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Alexmin9',
    maintainer_email='alexandre.minvielle@estaca.eu',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'Control_node = crazyflie.Control_node:main',
            'interface_node_vrai = crazyflie.interface_node_vrai:main',
        ],
    },
)
