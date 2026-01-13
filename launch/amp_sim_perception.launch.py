import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess , TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch_ros.actions import Node

def generate_launch_description():

    
    yolo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('yolobot_recognition'), 'launch'),
            '/launch_yolov8.launch.py'
        ]),
        launch_arguments={'image':"/oak/left/image_raw",
                          'inferenceresult':"/Yolov8_Inference",
                          'inferenceimg':"/image/inference",
                          'namespace':"/AMP"}.items()

    )


    perception = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('perception'),'launch'),
            '/amp_sim.launch.py'
            ]),
            launch_arguments={'camera/left':"/oak/left/image_raw",
                              'camera/right':"/oak/right/image_raw",
                              'disparity':"/sm2/disparity/disparity_image",
                              'disparity':"/oak/stereo/image_raw",
                              'inference':"/Yolov8_Inference",
                              'track':"/position_estimation/track",
                              'pointcloud':"/position_estimation/point_cloud",
                              'namespace':"/AMP"}.items()
            
            
    )
    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper.launch.py'
            ]),
            launch_arguments={'odom':'/orbslam/odom',
                              'track':"/track",
                              'track_pub':"/mapper/track",
                              'namespace':"/AMP"}.items()
                              
    )

    track_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros2_mapper'),'launch'),
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
            launch_arguments={'left_image':"/oak/left/image_raw",
                              'right_imgae':"/oak/right/image_raw",
                              '/params':"/home/carlosmello/ws/src/passive_stereo/cfg/stereo_rgb_heavy_sim.yaml"}.items()
    )
    
    
    
   
    return LaunchDescription([
        mapper,
        perception,
        foxglove,
        yolo,
        #slam,
        disparity,
        TimerAction(
            period=15.0,  # Delay in seconds
            actions=[fsds],
        )])


