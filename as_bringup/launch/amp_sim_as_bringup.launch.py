'''Launcher para ser usado nas simulações para o Shakedown com o simulador'''

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
        launch_arguments = {'UDP_control':"True", 'mission_name':"skidpad"}.items()
    )

    point = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('as_utils'), 'launch'),
            '/pointcloud_rgb.launch.py'
        ]),
        launch_arguments={'track':"/testing_only/track", 'frame_id':"fsds/map"}.items()
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
            get_package_share_directory('ros2_mapper'),'launch'),
            '/mapper.launch.py'
            ]),
            launch_arguments={'odom':'/fsds/testing_only/odom',
                              'track':"/position_estimation/track",
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
            launch_arguments={'left_image':"/fsds/cameracam2/image_color",
                              'right_imgae':"/fsds/cameracam1/image_color",
                              '/params':"/home/carlosmello/ws/src/passive_stereo/cfg/stereo_rgb_heavy_sim.yaml"}.items()
    )

    return LaunchDescription([
        path,
        control,
        foxglove,
        fsds,
        point,
        yolo,
        perception,
        mapper,
        track_sim,
        disparity,
        TimerAction(
            period=5.0,  
            actions=[fsds],
        )
    ])