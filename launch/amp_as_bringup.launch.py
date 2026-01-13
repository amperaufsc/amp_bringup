''''Launcher para ser usado sem o simulador e durante o período de Shakedown'''


import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
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
                          'inferenceimg':"/yolov8/inference",
                          'namespace':"/AMP"
                           }.items()
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
                            'namespace':"/AMP"
                            }.items()
   )




    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('path_planning'), 'launch'),
            '/path_planning.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP",
                         'odom':"/odom",
                         'go': "/signal/go",
                         'track':"/track",
                         'path':"/path"
                         }.items()
   )




    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
           get_package_share_directory('control'), 'launch'),
           '/control.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",
                           'odom':"/odom",
                           'path':"/path",
                           'control':"/control_command"
                           }.items()
   )




    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper.launch.py'
            ]),
            launch_arguments={'odom':'/odom',
                            'track':"/position_estimation/track",
                            'track_pub':"/mapper/track",
                            'namespace':"/AMP"
                            }.items()
   )




    ouster_ros = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ouster_ros'),'launch'),
            '/driver.launch.py'
            ]),
            launch_arguments={'odom':'/odom',
                            'track':"/position_estimation/track",
                            'track_pub':"/mapper/track",
                            'namespace':"/AMP"
                            }.items()
   )




    as_utils = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('as_utils'),'launch'),
            '/pointcloud_rgb.launch.py'
            ]),
            launch_arguments={'track':"/track",
                            'pointcloud':"/pointcloud",
                            'namespace':"/AMP"
                            }.items()
   )




    as_state = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('as_state'),'launch'),
            '/state.launch.py'
            ]),
            launch_arguments={'ebs':"/std_msgs/ebs",
                            'ts_active':"/std_msgs/ts_active",
                            'r2d':"/std_msgs/r2d",
                            'brake':"/std_msgs/brake",
                            'sdc':"/std_msgs/sdc",
                            'MF':"/std_msg/MF",
                            'state':"/std_msg/state",
                            'namespace':"/AMP"
                            }.items()
   )




    lidar_filtering = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('lidar_filtering'),'launch'),
            '/camera_lidar.launch.py.launch.py'
            ]),
            launch_arguments={'image_sub':"/cameracam2/image_color",
                            'lidar_sub':"/lidar/Lidar1",
                            'lidar_sub':"/fusion/lidar_camera",
                            'namespace':"/AMP"
                            }.items()
   )




    state_estimation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('state_estimation'),'launch'),
            '/state_estimation.launch.py'
            ]),
            launch_arguments={'odom':'/odom',
                            'imu':"/imu",
                            'wheel':"/wheel",
                            'namespace':"/AMP"
                            }.items()
   )




    yolobot_recognition = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('yolobot_recognition'),'launch'),
            '/launch_yolov8.launch.py'
            ]),
            launch_arguments={'image':'/image',
                            'inferenceresult':"/inferenceresult",
                            'inferenceimg':"/inferenceimg",
                            'namespace':"/AMP"
                            }.items()
   )




    return LaunchDescription([
        depthai,
        yolo,
        perception,
        path,
        control,
        mapper,
        as_utils,
        as_state,
        ouster_ros,
        lidar_filtering,
        state_estimation,
        yolobot_recognition
  ])