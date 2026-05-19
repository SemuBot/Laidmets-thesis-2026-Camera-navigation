from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, EqualsSubstitution
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg = get_package_share_directory('semubot_camera_navigation')

    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='false')
    use_sim_time = LaunchConfiguration('use_sim_time')

    slam_arg = DeclareLaunchArgument(
        'slam',
        default_value='rtabmap',
        description='Which SLAM backend to launch: rtabmap (default) or toolbox (sim only, requires encoders)'
    )
    slam = LaunchConfiguration('slam')

    depthimage_to_laserscan = Node(
        package='depthimage_to_laserscan',
        executable='depthimage_to_laserscan_node',
        name='depthimage_to_laserscan',
        output='screen',
        parameters=[{
            'scan_height': 30,
            'range_min': 0.1,
            'range_max': 5.0,
            'output_frame': 'base_link',
            'use_sim_time': use_sim_time,
        }],
        remappings=[
            ('depth', '/camera/aligned_depth_to_color/image_raw'),
            ('depth_camera_info', '/camera/color/camera_info'),
            ('scan', '/scan'),
        ]
    )

    ekf = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_node',
        output='screen',
        parameters=[os.path.join(pkg, 'config', 'ekf.yaml'), {'use_sim_time': use_sim_time}],
        condition=IfCondition(EqualsSubstitution(slam, 'toolbox')),
    )

    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('slam_toolbox'),
                'launch',
                'online_async_launch.py'
            )
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam_params_file': os.path.join(pkg, 'config', 'slam_toolbox_params.yaml')
        }.items(),
        condition=IfCondition(EqualsSubstitution(slam, 'toolbox')),
    )

    rtabmap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'rtabmap_bringup.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
        condition=IfCondition(EqualsSubstitution(slam, 'rtabmap')),
    )

    return LaunchDescription([
        use_sim_time_arg,
        slam_arg,
        ekf,
        depthimage_to_laserscan,
        slam_toolbox,
        rtabmap,
    ])
