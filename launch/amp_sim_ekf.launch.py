import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    ekf = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('kalman_filter'), 'launch'),
            '/kalman_filter_sim.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP",
                          'odometry':"/fsds/testing_only/odom",
                          'imu': "/fsds/imu",
                          'ekf_odometry':"/ekf_odometry",
                          'freq_pub':"/frequency/ekf_odom"}.items()
    )
    
 
    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('path_planning'), 'launch'),
            '/path_planning.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP", 'odom':"/orbslam/odom", 'go': "/signal/go", 'track':"/mapper/track"}.items()
    )

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('control'), 'launch'),
            '/control.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",'odom':"/orbslam/odom", 
                            'control':"/control_command"
                            }.items()
    )

    return LaunchDescription([
        ekf
    ])



