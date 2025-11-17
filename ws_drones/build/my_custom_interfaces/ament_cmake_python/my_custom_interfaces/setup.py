from setuptools import find_packages
from setuptools import setup

setup(
    name='my_custom_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('my_custom_interfaces', 'my_custom_interfaces.*')),
)
