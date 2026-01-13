import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    foxglove = Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            output='screen'
    )

    state_estimation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('state_estimation'), 'launch'),
            '/estimation_node.launch.py'
        ]),
        launch_arguments={'rec_odom':"/testing_only/odom", 'track':"/testing_only/track"}.items()
    )

    fsds = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('fsds_ros2_bridge'), 'launch'),
            '/fsds_ros2_bridge.launch.py'
        ]),
        launch_arguments = {'UDP_control':"True", 'mission_name':"acceleration"}.items()
    )

    return LaunchDescription([
        state_estimation,
        foxglove,
        TimerAction(
            period=5.0,  # Delay in seconds
            actions=[fsds],
        )
    ])