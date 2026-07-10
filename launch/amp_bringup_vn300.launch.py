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

    depthai = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        os.path.join(
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

    vectornav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('vectornav'),'launch'),
            '/vectornav.launch.py'
            ])                         
    )

    vectornav_msgs = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('robot_localization'),'launch'),
            '/vectornav_msgs.launch.py'
            ]),
            launch_arguments={'Imu_sub':'/vectornav/raw/imu',
                              'Ins_sub':'/vectornav/raw/ins',
                              'Attitude_sub':'/vectornav/raw/attitude'}.items()               
    )

    ekf_odom = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('robot_localization'),'launch'),
            '/dual_ekf_amp.launch.py'
            ])                
    )

    mapper = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('mapper'),'launch'),
        '/mapper.launch.py'
        ]),
        launch_arguments={'odom':'/odometry/global',
                            'track':"/track",
                            'track_pub':"/mapper/track",
                            'namespace':"/AMP"}.items()
                              
    )

    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('path_planning'), 'launch'),
            '/path_planning.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP", 'odom':"/odometry/global", 'go': "/signal/go", 'track':"/mapper/track"}.items()
    )

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('control'), 'launch'),
            '/control.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",'odom':"/odometry/global", 
                            'control':"/control_command",
                            'reference_path':"/control/reference"
                            }.items()
    )
    
    # can = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([os.path.join(
    #         get_package_share_directory('can_bus'),'launch'),
    #         '/can_jetson.launch.py'
    #         ]),
    # )
    
   
    return LaunchDescription([
        
        ExecuteProcess(
            cmd=['/opt/ros/humble/lib/tf2_ros/static_transform_publisher',
                  '--yaw', '0',
                  '--roll', '0',
                  '--pitch', '0',
                  '--frame-id', 'vectornav',
                  '--child-frame-id', 'base_link'],
            output='screen',),
             
        depthai,
        yolo,
        # perception,
        # vectornav,
        # vectornav_msgs,
        # ekf_odom,
        # mapper,
        # path,
        # control,
        # can
        
    ])