'''Launcher para ser usado nas simulações para o Shakedown com o simulador'''

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
                          'go': "/fsds/signal/go", 
                          'track':"/fsds/testing_only/track"}.items()
    )

    transform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('transformation_broadcast'),'launch'),
            '/amp_transformation.launch.py'
            ]),
            launch_arguments={'odom':"/fsds/testing_only/odom"}.items() #mudar topico 'odom' para /odom_with_error se for usar odom com erro forçado
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

    yolo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('yolobot_recognition'), 'launch'),
            '/launch_yolov8.launch.py'
        ]),
        launch_arguments={'image':"/fsds/cameracam2/image_color",
                          'inferenceresult':"/Yolov8_Inference",
                          'inferenceimg':"/image/inference",
                          'namespace':"/AMP"}.items()
    )

    perception = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('perception'),'launch'),
            '/amp_sim.launch.py'
            ]),
            launch_arguments={'camera/left':"/fsds/cameracam2/image_color",
                              'camera/right':"/fsds/cameracam1/image_color",
                              'disparity':"/sm2/disparity/disparity_image",
                              'inference':"/Yolov8_Inference",
                              'track':"/position_estimation/track",
                              'pointcloud':"/position_estimation/point_clound",
                              'namespace':"/AMP"}.items()      
    )

    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper.launch.py'
            ]),
            launch_arguments={'odom':'/fsds/testing_only/odom',
                              'track':"/track",
                              'track_pub':"/mapper/track",
                              'namespace':"/AMP"}.items()
    )

    track_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/sim_mapper.launch.py'
            ]),
            launch_arguments={'odom':'/fsds/testing_only/odom',
                              'track':"/fsds/testing_only/track",
                              'track_pub':"/track",
                              'namespace':"/AMP"}.items()
    )

    laserscan = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('pointcloud_to_laserscan'),'launch'),
            '/amp_pointcloud_to_laserscan.launch.py'
            ]),
            launch_arguments={'cloud_in':"/fsds/lidar/Lidar2",
                              'scan':"/scan"}.items()
    )

    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'),'launch'),
            '/online_async_launch.py'
            ])
    )

    ekf = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('robot_localization'),'launch'),
            '/ekf_amp.launch.py'
            ])
    )


    return LaunchDescription([
        ExecuteProcess(
            cmd=['/opt/ros/humble/lib/tf2_ros/static_transform_publisher',
                  '--yaw', '0',
                  '--roll', '0',
                  '--pitch', '0',
                  '--frame-id', 'fsds/map',
                  '--child-frame-id', 'fsds/odom'],
            output='screen',),
        path,
        control,
        laserscan,
        transform,
        slam_toolbox
    ])