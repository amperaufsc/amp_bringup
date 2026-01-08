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

    dir = f"/mnt/exfat/bag_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    depthai = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([os.path.join(
            FindPackageShare('depthai_ros_driver').find('depthai_ros_driver'), 
            'launch', 'camera.launch.py')
        ])
    )

    
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
            '/amp_perception.launch.py'
            ]),
            launch_arguments={'camera/left':"/oak/left/image_raw",
                              'camera/right':"/oak/right/image_raw",
                              'disparity':"/oak/stereo/image_raw",
                              'inference':"/Yolov8_Inference",
                              'track':"/track",
                              'namespace':"/AMP"}.items()
    )


    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros2_mapper'),'launch'),
            '/mapper.launch.py'
            ]),
            launch_arguments={'odom':"/orbslam/odom",
                              'track':"/track",
                              'track_pub':"/mapper/track",
                              'namespace':"/AMP"}.items()
    )


    orbslam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('orbslam3_ros2'),'launch'),
            '/amp_stereo.launch.py'
            ]),
            launch_arguments={'left_camera':"/oak/left/image_raw",
                          'right_camera':"/oak/right/image_raw",
                          'namespace':"/AMP"}.items()
    )


    odom = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros2_mapper'),'launch'),
            '/odometry.launch.py'
            ]),
            launch_arguments={'pose_sub':'/AMP/orbslam/pose',
                              'odom_pub':"/orbslam/odom"}.items()                    
    )

    return LaunchDescription([
        ExecuteProcess(
             cmd=['/opt/ros/humble/lib/tf2_ros/static_transform_publisher',
                  '--yaw', '0',
                  '--roll', '0',
                  '--pitch', '0',
                  '--frame-id', 'orbslam3',
                  '--child-frame-id', 'map'],
             output='screen',),
             
        depthai,
        orbslam,
        odom,
        yolo,
        perception,
        # TimerAction(
        #     period=10.0,  # Delay in seconds
        #     actions=[mapper])
    ])