from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, LogInfo, OpaqueFunction, EmitEvent
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition
import os
from lifecycle_msgs.msg import Transition, TransitionEvent, State
from ament_index_python.packages import get_package_share_directory

def final_status_check(context, *args, **kwargs):
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
    from lifecycle_msgs.srv import GetState

    rclpy.init()
    node = Node('bringup_supervisor')

    success = True
    required_nodes = ['position_estimator', 'path_node', 'control_node', 'mapper_node']
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
    perception_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('perception'), 'launch/lifecycle_dpe.launch.py')
        )
    )
    path_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('path_planning'), 'launch/path_lifecycle.launch.py')
        )
    )
    control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('control'), 'launch/control_lifecycle.launch.py')
        )
    )
    mapper_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('mapper'), 'launch/mapper_lifecycle.launch.py')
        )
    )

    state_machine_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('state_machine_as'), 'launch/state_node.launch.py')
        )
    )

    return LaunchDescription([
        state_machine_launch,
        perception_launch,
        path_launch,
        control_launch,
        mapper_launch,

        TimerAction(
            period=20.0,  # tempo para os nós se estabilizarem
            actions=[
                LogInfo(msg='Verificando estados finais...'),
                OpaqueFunction(function=final_status_check)
            ]
        )
    ])
