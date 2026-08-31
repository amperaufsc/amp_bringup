import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
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
        ),
        launch_arguments={'namespace': '',
                "path" : "path_concatenated"}.items()
    )

    low_level_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('control'), 'launch', 'low_level_control.launch.py')
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
        )
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
            os.path.join(get_package_share_directory('perception'), 'launch', 'amp_perception_lifecycle.launch.py')
        ),
        launch_arguments={'namespace':""}.items()
    )

    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('depthai_ros_driver'), 'launch', 'camera.launch.py')
        )
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
        orbslam3_launch,
        low_level_control_launch
        ])