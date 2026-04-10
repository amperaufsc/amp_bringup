import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true'
    )
    
    laserscan = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('pointcloud_to_laserscan'),'launch'),
            '/amp_pointcloud_to_laserscan.launch.py'
            ]),
            launch_arguments={'cloud_in':"/fsds/lidar/Lidar2",
                              'scan':"/scan",
                              'use_sim_time':use_sim_time}.items()
    )
    
    transform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('transformation_broadcast'),'launch'),
            '/amp_transformation.launch.py'
            ]),
            launch_arguments={'odom':"/odometry/filtered"}.items() #mudar topico 'odom' para /odom_with_error se for usar odom com erro forçado
    ) 

    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'),'launch'),
            '/online_async_launch.py'
            ]),
            launch_arguments={'use_sim_time':use_sim_time}.items()
    )

    ekf = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('robot_localization'),'launch'),
            '/ekf_amp.launch.py'
            ]),
            launch_arguments={'use_sim_time':use_sim_time}.items()
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        ekf,
        laserscan,
        slam_toolbox
    ])