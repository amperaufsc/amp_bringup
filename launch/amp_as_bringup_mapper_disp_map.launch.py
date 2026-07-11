import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction
from launch.actions import DeclareLaunchArgument as LaunchArg


def generate_launch_description():

    #
    #   Motion
    #
    path_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('path_planning'), 'launch', 'path_planning_lifecycle.launch.py')
        )
    )

    control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('control'), 'launch', 'control_lifecycle.launch.py')
        )
    )

    check_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('control'), 'launch', 'check_lifecycle.launch.py')
        )
    )

    # -- implementar can node --

    #
    #  

    #
    #   Mapper
    #
    mapper_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('mapper'), 'launch', 'mapper_lifecycle.launch.py')
        ),
        launch_arguments={'odom':'/orbslam/odom',
                          'track':'/track',
                          'track_pub':'/mapper/track'}.items()
    )

    odometry_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('mapper'), 'launch', 'odometry.launch.py')
        ),
        launch_arguments={'pose_sub':'/AMP/orbslam/pose',
                          'odom_pub':'/orbslam/odom'
                         }.items()
    )

    orbslam3_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('orbslam3_ros2'), 'launch', 'amp_stereo.launch.py')),
            launch_arguments={'left_camera':"/oak/left/image_raw",
                          'right_camera':"/oak/right/image_raw",
                          'frame_id':'orbslam3',
                          'namespace':"/AMP"}.items()
    )

    #
    # State Machine
    #
    state_machine_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('amp_sm'), 'launch', 'state_machine.launch.py')
        )
    )

    repeater_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('amp_sm'), 'launch', 'repeater_lifecycle.launch.py')
        ),
        launch_arguments={
                    # Subscribe topics
                    'mission_select_in' : "/as_amp/mission_select",
                    'go_in' : "/as_amp/res/go",
                    'ready_in' : "/as_amp/res/as_ready",
                    'emergency_in' : "/as_amp/res/as_emergency",
                    #Publish topics
                    'mission_go_out' : "/as_amp/mission_selected/go",
                    'go_out' : "/as_amp/res/go_out", 
                    'ready_out' : "/as_amp/res/as_ready_out",
                    'emergency_out' : "/as_amp/res/as_emergency_out",
                    'namespace':""
                    }.items()
    )

    can_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('amp_utils'), 'launch', 'can_pub.launch.py')
        ),
        launch_arguments={'autonomous_mode_topic' : "/as_amp/mission_select",
                    'as_status_topic' : "/as_amp/res/as_ready",
                    'go_signal_topic' : "/as_amp/res/go",
                    'emergency_topic' : "/as_amp/res/as_emergency",
                    'namespace':""
                    }.items()
    )

    #
    #

    delayed_smacc_launch = TimerAction(
        period=25.0,
        actions=[LogInfo(msg="Tempo Acabou !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"),
                 state_machine_launch]
    )

    #
    #   Perception
    #
    perception_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('perception'), 'launch', 'amp_disp_perception_lifecycle.launch.py')
        ),
        launch_arguments={
            "camera/left":"/oak/left/image_raw",
            "camera/right":"/oak/right/image_raw",
            "disparity":"/disparity",
            'namespace':""}.items()
    )

    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('depthai_ros_driver'), 'launch', 'camera.launch.py')
        )
    )

    disparity_map_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('perception'), 'launch', 'amp_disparity_pub.launch.py')
        ),
        launch_arguments={
            "disparity":"/disparity",
            'namespace':""}.items()
    )

    yolo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('yolobot_recognition'), 'launch', 'yolov8_lifecycle.launch.py')
        ),
        launch_arguments={'namespace':""}.items()
    )
    

    # -- implementar transformacoes --

    #
    #

    return LaunchDescription([
        LogInfo(msg="=== INICIANDO O BRINGUP DO SISTEMA ==="),
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
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_orbslam_tf',
            arguments=[
                '--x', '0', '--y', '0', '--z', '0',
                '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '0',
                '--frame-id', 'map',
                '--child-frame-id', 'orbslam3'
            ]
        ),
        camera_launch,
        yolo_launch,
        perception_launch,
        path_launch,
        mapper_launch,
        control_launch,
        repeater_launch,
        odometry_launch,
        can_launch,
        check_launch,
        delayed_smacc_launch,
        disparity_map_launch,
        orbslam3_launch
        ])