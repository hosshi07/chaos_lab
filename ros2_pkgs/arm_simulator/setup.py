from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'arm_simulator'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # urdf/assetsフォルダ内のすべてのSTLファイルをインストール
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'urdf/assets'), glob('urdf/assets/*.stl')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ts',
    maintainer_email='tosshi1229@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'so101_simulator_node = arm_simulator.so101_simulator_node:main'
        ],
    },
)
