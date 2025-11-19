from setuptools import find_packages, setup

package_name = 'crflie_test'

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
    maintainer='estacalab',
    maintainer_email='estacalab@todo.todo',
    description='TODO: Package description',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'Mocap_node = crflie_test.Mocap:main',
            'Control_node = crflie_test.Control:main'
        ],
    },
)
