import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess , TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch_ros.actions import Node

def generate_launch_description():
  
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros2_mapper'),'launch'),
            '/mapper.launch.py'
            ]),
            launch_arguments={'odom':'/orbslam/odom',
                              'track':"/track",
                              'track_pub':"/mapper/track",

                              'namespace':"/AMP"}.items()
    )
    track_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper_test.launch.py'
            ]),
            launch_arguments={'odom':'/fsds/testing_only/odom',
                              'track':"/fsds/testing_only/track",
                              'track_pub':"/position_estimation/track",
                              'namespace':"/AMP"}.items()
    )
    disparity = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('disparity'),'launch'),
            '/fsds_disparity.launch.py'
            ]),
            launch_arguments={'left_image':"/fsds/cameracam2/image_color",
                              'right_imgae':"/fsds/cameracam1/image_color",
                              '/params':"/home/carlosmello/ws/src/passive_stereo/cfg/stereo_rgb_heavy_sim.yaml"}.items()
    )
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('orbslam3_ros2'),'launch'),
            "/amp_stereo_sim.launch.py"
            ]),
            launch_arguments={'/camera/left':"/oak/left/image_raw",
                              '/camera/right':"/oak/right/image_raw"

            }.items()

                              'namespace':"/AMP"}.items()                  

    )
   
    return LaunchDescription([
       mapper
    ])