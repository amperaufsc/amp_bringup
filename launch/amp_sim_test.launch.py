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

    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/mapper.launch.py'
            ]),
            launch_arguments={'odom':'/orbslam/odom',
                              'track':"/track",
                              'track_pub':"/mapper/track",
                              'namespace':"/AMP"}.items()                        
    )

    passivo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('disparity'),'launch'),
            '/fsds_disparity.launch.py'
            ]),
            launch_arguments={'left_image':'/left/image_raw',
                              'right_image':"/right/image_raw",
                              'left_info':"/left/camera_info",
                              'right_info':"/right/camera_info",
                              'stereo_params':"/params",
                              'namespace':"/AMP"}.items()             
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('orbslam3_ros2'), 'launch'),
            '/amp_stereo.launch.py'
        ]),
        launch_arguments={'left_camera':"/oak/left/image_raw",
                          'right_camera':"/oak/right/image_raw",
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
                             'inference':"/Yolov8_Teste_Inference",
                             'track':"/position_estimation/teste_track",
                             'pointcloud':"/position_estimation/point_cloud",
                             'namespace':"/AMP"}.items()   
   )

    odom = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/odometry.launch.py'
            ]),
            launch_arguments={'pose_sub':'/AMP/orbslam/pose',
                              'odom_pub':"/orbslam/odom"}.items()                   
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
    
 
    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('path_planning'), 'launch'),
            '/path_planning.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP", 'odom':"/orbslam/odom", 'go': "/signal/go", 'track':"/mapper/track"}.items()
    )

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('control'), 'launch'),
            '/control.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",'odom':"/orbslam/odom", 
                            'control':"/control_command"
                            }.items()
    )

    fsds = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('fsds_ros2_bridge'), 'launch'),
            '/fsds_ros2_bridge.launch.py'
        ]),
        launch_arguments = {'UDP_control':"True", 'mission_name':"acceleration"}.items()
    )

    point = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('as_utils'), 'launch'),
            '/pointcloud_rgb.launch.py'
        ]),
        launch_arguments={'track':"/mapper/track", 'frame_id':"fsds/map"}.items()
    )

    return LaunchDescription([
        path,
        control,
        #foxglove,
        point,
        mapper,
        odom, 
        slam,
        perception,
        yolo,
        passivo,
        TimerAction(
            period=5.0,  # Delay in seconds
            actions=[fsds],
        )
    ])



