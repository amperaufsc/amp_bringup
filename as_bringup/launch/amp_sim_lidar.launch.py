import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess , TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch_ros.actions import Node

def generate_launch_description():
    lidar_filtering = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('lidar_filtering'),'launch'),
            '/camera_lidar.launch.py'
            ]),
            launch_arguments={''
            #'camera_sub':"/fsds/cameracam2/camera_info",
                              'image_sub':"/fsds/cameracam2/image_color",
                              'lidar_sub':"/fsds/lidar/Lidar1",
                              'image_pub':"/fusion/lidar_camera",}.items()
            )
    return LaunchDescription([lidar_filtering])