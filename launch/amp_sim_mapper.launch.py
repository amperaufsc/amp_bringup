import os
import datetime
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess , TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch_ros.actions import Node


def generate_launch_description():

    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper.launch.py'
        ]),
        launch_arguments={'track':"/track",
                          'track_pub':"/mapper/track",
                          'odom':"/fsds/testing_only/odom",
                          'namespace':"/AMP"}.items()
    )
    
    sim_mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/sim_mapper.launch.py'
        ]),
        launch_arguments={'track':"/fsds/testing_only/track",
                          'track_pub':"/track",
                          'odom':"/fsds/testing_only/odom",
                          'namespace':"/AMP"}.items()
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=['/opt/ros/humble/lib/tf2_ros/static_transform_publisher',
                  '--yaw', '0',
                  '--roll', '0',
                  '--pitch', '0',
                  '--frame-id', 'left_camera_link',
                  '--child-frame-id', 'oak_left_camera_optical_frame'],
            output='screen',),
        sim_mapper,
        TimerAction(
            period=10.0,  # Delay in seconds
            actions=[mapper]),
    ])