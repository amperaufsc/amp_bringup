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
from launch_ros.actions import SetParameter
from launch_ros.actions import Node


def generate_launch_description():

    vectornav_msgs = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('state_estimation'), 'launch'),
            '/vectornav_msgs.launch.py'
        ]),
        launch_arguments={'Imu_sub':"/vectornav/raw/imu",
                          'Ins_sub':"/vectornav/raw/ins",
                          'Attitude_sub':"/vectornav/raw/attitude"}.items()
    )

    ekf = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('robot_localization'), 'launch'),
            '/ekf.launch.py'
        ])
    )

    navsat_transform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('robot_localization'), 'launch'),
            '/navsat_transform.launch.py'
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

    camera_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='camera_static_tf',
        arguments=['0.0','0.0','0.0',
                    '0.0','0.0','0.0',
                    'odom','oak-d-base-frame']
    )

    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper.launch.py'
        ]),
        launch_arguments={'track':"/track",
                          'track_pub':"/mapper/track",
                          'odom':"/odometry/filtered",
                          'namespace':"/AMP"}.items()
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('slam_toolbox'), 'launch'),
            '/online_async_launch.py'
        ])
    )

    pointcloud = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('amp_utils'),'launch'),
            '/pointcloud_rgb.launch.py'
            ]),
            launch_arguments={'track':"/track",
                              'pointcloud':"/track/pointcloud"}.items()
    )

    laserscan = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('pointcloud_to_laserscan'),'launch'),
            '/amp_pointcloud_to_laserscan.launch.py'
            ]),
            launch_arguments={'cloud_in':"/track/pointcloud",
                              'scan':"/scan"}.items()
    )
    
    transform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('transformation_broadcast'),'launch'),
            '/amp_transformation.launch.py'
            ]),
            launch_arguments={'odom':"/odometry/filtered"}.items() #mudar topico 'odom' para /odom_with_error se for usar odom com erro forçado
    ) 
    

    odom = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/odometry.launch.py'
            ]),
            launch_arguments={'pose_sub':'/pose',
                              'odom_sub':'/fsds/testing_only/odom',
                              'odom_pub':"/slam_toolbox/odom"}.items()                    
    )
    

    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('path_planning'), 'launch'),
            '/path_planning.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP", 'odom':"/fsds/testing_only/odom", 'go': "/signal/go", 'track':"/fsds/testing_only/track"}.items()
    )
     

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('control'), 'launch'),
            '/control.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",'odom':"/fsds/testing_only/odom", 
                            'control':"/fsds/control_command",
                            'path':"/AMP/path",
                            'reference_path':"/control/reference"
                            }.items()
    )

    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),
        ExecuteProcess(
            cmd=['/opt/ros/humble/lib/tf2_ros/static_transform_publisher',
                  '--yaw', '0',
                  '--roll', '0',
                  '--pitch', '0',
                  '--frame-id', 'base_link',
                  '--child-frame-id', 'oak-d-base-frame'],
            output='screen',),
        vectornav_msgs,
        ekf,
        navsat_transform,
        yolo,
        perception,
        mapper,
        pointcloud,
        #laserscan,
        #transform,
        #slam,
        # odom,
        # path,
        # control
    ])