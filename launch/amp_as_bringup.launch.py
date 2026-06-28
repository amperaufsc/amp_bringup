import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction

def generate_launch_description():

    #
    #   Motion
    #
    path_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('path_planning'), 'launch', 'path_planning.launch.py')
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
        )
    )

    odometry_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('mapper'), 'launch', 'odometry.launch.py')
        )
    )

    # -- implementar o Orb Slam --

    #
    #


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
        )
    )
    #
    #

    delayed_smacc_launch = TimerAction(
        period=10.0,
        actions=[LogInfo(msg="Tempo Acabou !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"),
                 state_machine_launch]
    )

    #
    #   Perception
    #
    perception_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('perception'), 'launch', 'amp_perception_lifecycle.launch.py')
        )
    )

    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('depthai_ros_driver'), 'launch', 'camera.launch.py')
        )
    )

    yolo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('yolobot_recognition'), 'launch', 'yolov8_lifecycle.launch.py')
        )
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
        control_launch,
        repeater_launch,
        odometry_launch,
        check_launch,
        delayed_smacc_launch
        ])