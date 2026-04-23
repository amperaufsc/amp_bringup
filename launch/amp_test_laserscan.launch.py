import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    
    laserscan = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('pointcloud_to_laserscan'),'launch'),
            '/amp_pointcloud_to_laserscan.launch.py'
            ]),
            launch_arguments={'cloud_in':"/fsds/lidar/Lidar1",
                              'scan':"/scan"}.items()
    )
    
    transform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('transformation_broadcast'),'launch'),
            '/amp_transformation.launch.py'
            ]),
            launch_arguments={'odom':"/fsds/testing_only/odom"}.items() #mudar topico 'odom' para /odom_with_error se for usar odom com erro forçado
    ) 

    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'),'launch'),
            '/online_async_launch.py'
            ]),
            launch_arguments={'scan':"/scan",
                              'scan_visualization':"/slam_toolbox/scan_visualization",
                              'graph_visualization':"/slam_toolbox/graph_visualization",
                              'map':"/map",
                              'tf':"/tf",
                              }.items() 

    ) 

    return LaunchDescription([
        laserscan,
        slam_toolbox
    ])