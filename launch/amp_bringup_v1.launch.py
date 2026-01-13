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
from lifecycle_msgs.msg import Transition, TransitionEvent, State
from launch.actions import IncludeLaunchDescription, TimerAction, LogInfo, OpaqueFunction, EmitEvent


def final_status_check(context, *args, **kwargs):
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
    from lifecycle_msgs.srv import GetState

    rclpy.init()
    node = Node('bringup_supervisor')

    success = True
    required_nodes = ['perception_node', 'path_node', 'control_node', 'mapper_node']
    client_map = {}

    for n in required_nodes:
        client = node.create_client(GetState, f'/{n}/get_state')
        if not client.wait_for_service(timeout_sec=2.0):
            node.get_logger().error(f"Nó {n} não responde ao get_state")
            success = False
            #break
        client_map[n] = client

    for name, client in client_map.items():
        req = GetState.Request()
        future = client.call_async(req)
        rclpy.spin_until_future_complete(node, future, timeout_sec=2.0)
        if future.result() is None or future.result().current_state.label != 'active':
            node.get_logger().warn(f"Nó {name} não está ativo. Estado atual: {future.result().current_state.label if future.result() else 'desconhecido'}")
            success = False

    pub = node.create_publisher(String, '/fsm_signal', 10)
    transition_event_pub = node.create_publisher(TransitionEvent, '/EvSystemChecksOK', 10)

    msg = String()
    event = TransitionEvent()
    msg.data = "Ready" if success else "NOT READY"
    node.get_logger().info(f"Publicando sinal final: {msg.data}")
    pub.publish(msg)
    if msg.data == "Ready":
        transition_event_pub.publish(event) #Envia o sinal que transiciona do As_Off para As_Ready la no state_machine_as

    rclpy.shutdown() # nao sei se isso se mantem ou nao
    return []

def generate_launch_description():

    dir = f"/mnt/exfat/bag_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    depthai = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        os.path.join(
            FindPackageShare('depthai_ros_driver').find('depthai_ros_driver'), 
            'launch', 'camera.launch.py')
        ])
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
            '/lifecycle_dpe_v1.launch.py'
            ]),
            launch_arguments={'camera/left':"/oak/left/image_raw",
                              'camera/right':"/oak/right/image_raw",
                              'disparity':"/oak/stereo/image_raw",
                              'inference':"/Yolov8_Inference",
                              'track':"/track",
                              'namespace':"/AMP"}.items()
    )

    mapper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mapper'),'launch'),
            '/lifecycle_mapper_v1.launch.py'
            ]),
            launch_arguments={'odom':'/orbslam/odom',
                              'track':"/track",
                              'track_pub':"/mapper/track",
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
    
    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('path_planning'), 'launch'),
            '/path_lifecycle_v1.launch.py'
        ]),
        launch_arguments={'namespace':"/AMP", 'odom':"/orbslam/odom", 'go': "/signal/go", 'track':"/mapper/track"}.items()
    )
     
    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('control'), 'launch'),
            '/control_lifecycle_v1.launch.py',
        ]),
        launch_arguments = {'namespace':"/AMP",
                            'odom':"/orbslam/odom", 
                            'control':"/control_command",
                            'path':"/AMP/path"
                            }.items()
    )
    
    can = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('can_bus'),'launch'),
            '/can_jetson.launch.py'
            ]),
    )

    return LaunchDescription([
 
             
        depthai,
        slam,
        odom,
        yolo,
        perception,
        TimerAction(
            period=10.0,  # Delay in seconds
            actions=[mapper]),
        path,
        can,
        control,
        TimerAction(
            period=20.0,  # tempo para os nós se estabilizarem
            actions=[
                LogInfo(msg='Verificando estados finais...'),
                OpaqueFunction(function=final_status_check)
            ]
        )
        
    ])