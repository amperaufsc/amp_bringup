import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():



    scan = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('pointcloud_to_laserscan'), 'launch'),
            '/amp_pointcloud_to_laserscan.launch.py'
        ]),
        launch_arguments={'cloud_in':"/fsds/lidar/Lidar1",
                           'scan':"/scan"}.items()
    )

    transformation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('transformation_broadcast'), 'launch'),
            '/amp_transformation.launch.py'
        ]),
            launch_arguments={'odom':"/ekf/composed_odom"}.items()
    )

    ekf = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('kalman_filter'), 'launch'),
            '/kalman_filter.launch.py'
        ]),
        launch_arguments={'pose':"/pose",
                          'odometry':"/fsds/testing_only/odom",
                           'imu':"/fsds/imu",
                           'ekf_odometry':"/ekf/odom"}.items()
    )

    ekf_odom = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('state_estimation'), 'launch'),
            '/ekf_odom_sim.launch.py'
        ]),
        launch_arguments={'Ekf_odom_sub':"/ekf/odom",
                           'fsds_odom_sub':"/fsds/testing_only/odom",
                           'odom_pub':"/ekf/composed_odom"}.items()
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join( 
            get_package_share_directory('slam_toolbox'), 'launch'),
            '/online_async_launch.py'
        ])
    )



    return LaunchDescription([
        scan,
        transformation,
        ekf,
        ekf_odom,
        slam
    ])