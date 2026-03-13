import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    orbslam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('orbslam3_ros2'),'launch'),
            '/amp_stereo.launch.py'
            ]),
            launch_arguments={'left_camera':"/oak/left/image_raw",
                            'right_camera':"/oak/right/image_raw"}.items()
    )

    orbslam_odom = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('state_estimation'),'launch'),
            '/composed_slam_odom.launch.py'
            ]),
            launch_arguments={'pose_sub':"/orbslam/pose",
                              'Ins_sub':"/vectornav/raw/ins",
                              'Imu_sub':"/vectornav/raw/imu",
                              'Attitude_sub':"/vectornav/raw/attitude",
                              'odom_pub':"/odom"}.items()
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
    
    pointcloud = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('amp_utils'),'launch'),
            '/amp_pointcloud_to_laserscan.launch.py'
            ]),
            launch_arguments={'track':"/track",
                              'pointcloud':"/track_pointcloud"}.items()
    )

    laserscan = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('pointcloud_to_laserscan'),'launch'),
            '/amp_pointcloud_to_laserscan.launch.py'
            ]),
            launch_arguments={'cloud_in':"/track_pointcloud",
                              'scan':"/scan"}.items()
    )
    
    transform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('transformation_broadcast'),'launch'),
            '/amp_transformation.launch.py'
            ]),
            launch_arguments={'odom':"/orbslam/odom"}.items() #mudar topico 'odom' para /odom_with_error se for usar odom com erro forçado
    ) 

    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'),'launch'),
            '/online_async_launch.py'
            ])
    ) 

    return LaunchDescription([
        # yolo,
        # perception,
        # pointcloud,
        #orbslam,
        orbslam_odom,
        # laserscan,
        # transform,
        # slam_toolbox
    ])