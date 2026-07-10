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

    orbslam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('orbslam3_ros2'),'launch'),
            '/amp_stereo.launch.py'
            ])                         
    )

    orbslam_odom = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/odometry.launch.py'
            ]),
            launch_arguments={'pose_sub':'/orbslam/pose2',
                              'odom_pub':"/orbslam/odom"}.items()                    
    )

    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper_lifecycle.launch.py'
            ]),
            launch_arguments={'track':'/track',
                              'odom':"/orbslam/odom",
                              'track_pub':"/mapper/track"}.items()                    
    )


    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('path_planning'), 'launch'),
            '/path_planning.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP",
                          'odom':"/orbslam/odom", 
                          'go': "/signal/go", 
                          'track':"/mapper/track"}.items()
    )

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('control'), 'launch'),
            '/control.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",'odom':"/orbslam/odom", 
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
        
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='left_camera_optical_tf',
            arguments=[
                '--x', '0', '--y', '0', '--z', '0',
                '--qx', '-0.5', '--qy', '0.5', '--qz', '-0.5', '--qw', '0.5',
                '--frame-id', 'left_camera_link',
                '--child-frame-id', 'oak_left_camera_optical_frame'
            ]
        ),
        depthai,
        yolo,
        perception,
        orbslam,
        orbslam_odom,
        mapper,
        path,
        control,
        # can
        
    ])