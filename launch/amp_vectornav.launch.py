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

    vectornav = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        os.path.join(
            FindPackageShare('vectornav').find('vectornav'), 
            'launch', 'vectornav.launch.py')
        ])
    )

    pose = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('state_estimation'), 'launch'),
            '/vectornav_pose.launch.py'
        ]),
        launch_arguments={'input_pose':"/vectornav/pose",
                          'output_pose':"/corrected_pose"}.items()
    )


   
    return LaunchDescription([
        vectornav,
        pose
    ])