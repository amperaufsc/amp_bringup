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

    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('ros2_path_planning'), 'launch'),
            '/path_planning.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP", 'odom':"/testing_only/odom", 'go': "/signal/go", 'track':"/testing_only/track"}.items()
    )

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('ros2_control'), 'launch'),
            '/control.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",'odom':"/testing_only/odom", 
                            'control':"/control_command"
                            }.items()
    )

    fsds = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('fsds_ros2_bridge'), 'launch'),
            '/fsds_ros2_bridge.launch.py'
        ]),
        launch_arguments = {'UDP_control':"True", 'mission_name':"trackdrive"}.items()
    )

    point = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('as_utils'), 'launch'),
            '/pointcloud_rgb.launch.py'
        ]),
        launch_arguments={'track':"/testing_only/track", 'frame_id':"fsds/map"}.items()
    )

    return LaunchDescription([
        path,
        control,
        #foxglove,
        point,
        TimerAction(
            period=5.0,  # Delay in seconds
            actions=[fsds],
        )
    ])