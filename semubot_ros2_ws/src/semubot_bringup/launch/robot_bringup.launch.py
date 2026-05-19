from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, EqualsSubstitution
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    nav_arg = DeclareLaunchArgument(
        'nav',
        default_value='false',
        description='Launch nav2 stack alongside SLAM (set true when map is ready)'
    )
    nav = LaunchConfiguration('nav')

    slam_arg = DeclareLaunchArgument(
        'slam',
        default_value='rtabmap',
        description='Which SLAM backend to launch: rtabmap (default) or toolbox (slam_toolbox)'
    )
    slam = LaunchConfiguration('slam')

    # Robot description
    xacro_file = os.path.join(
        get_package_share_directory('semubot_description'),
        'urdf',
        'semubot.urdf.xacro'
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['xacro ', xacro_file]),
                value_type=str
            ),
            'use_sim_time': False,
        }]
    )

    camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('semubot_bringup'),
                'launch',
                'camera.launch.py'
            )
        ),
    )

    odom_broadcaster = Node(
        package='semubot_bringup',
        executable='odom_broadcaster.py',
        name='odom_broadcaster',
        output='screen',
        condition=IfCondition(EqualsSubstitution(slam, 'toolbox')),
    )

    # SLAM + EKF + depthimage_to_laserscan

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('semubot_camera_navigation'),
                'launch',
                'slam_bringup.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': 'false', 'slam': slam}.items()
    )

    # Nav2 (optional, enable with nav:=true)

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('semubot_camera_navigation'),
                'launch',
                'nav2_bringup.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': 'false'}.items(),
        condition=IfCondition(nav)
    )

    return LaunchDescription([
        nav_arg,
        slam_arg,
        joint_state_publisher,
        robot_state_publisher,
        camera,
        odom_broadcaster,
        slam_launch,
        nav2,
    ])
