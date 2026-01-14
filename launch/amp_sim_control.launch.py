import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('path_planning'), 'launch'),
            '/path_planning.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP", 
                          'odom':"/fsds/testing_only/odom", 
                          'go': "/signal/go", 
                          'track':"/fsds/testing_only/track",
                          'path':"/path",
                          'path_concatenated':"/path_concatenated"}.items()
    )

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('control'), 'launch'),
            '/control.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",
                            'odom':"/fsds/testing_only/odom", 
                            'path':"/AMP/path_concatenated",
                            'control':"/fsds/control_command"
                            }.items()
    )
    '''
    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper.launch.py'
            ]),
            launch_arguments={'namespace':"/AMP",
                            'odom':'/fsds/testing_only/odom',
                            'track':"/sim_mapper/track",
                            'track_pub':"/mapper/track"
                            }.items()
   )
    
    sim_mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/sim_track.launch.py'
            ]),
            launch_arguments={'namespace':"/AMP",
                            'odom':'/fsds/testing_only/odom',
                            'track':"/fsds/testing_only/track",
                            'track_pub':"/sim_mapper/track"
                            }.items()
   )
    '''
    return LaunchDescription([
        path,
        control
        #sim_mapper,
        #mapper        
    ])