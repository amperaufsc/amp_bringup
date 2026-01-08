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

    can = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('can_bus'),'launch'),
            '/can_jetson.launch.py'
            ]),
    )

    
    bag = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('can_bus'),'launch'),
            '/bag_record.launch.py'
            ]),
    )
    depthai = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        os.path.join(
            FindPackageShare('depthai_ros_driver').find('depthai_ros_driver'), 
            'launch', 'camera.launch.py')
        ])
    )
    
    
   
    return LaunchDescription([
        can,
        bag,
        #depthai
        

        
        
    ])
