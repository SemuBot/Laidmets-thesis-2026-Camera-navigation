import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterFile


def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='false')
    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=PathJoinSubstitution([
            FindPackageShare('semubot_camera_navigation'), 'config', 'nav2_params.yaml'
        ])
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    params = ParameterFile(
        param_file=LaunchConfiguration('params_file'),
        allow_substs=True
    )

    nav2_params = [params, {'use_sim_time': use_sim_time}]

    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=nav2_params,
    )

    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=nav2_params,
        arguments=['--ros-args', '--log-level', 'info'],
    )

    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=nav2_params,
    )

    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=nav2_params,
    )

    waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=nav2_params,
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart': True,
            'bond_timeout': 10.0,
            'node_names': [
                'controller_server',
                'planner_server',
                'behavior_server',
                'bt_navigator',
                'waypoint_follower',
            ],
        }],
    )

    return LaunchDescription([
        use_sim_time_arg,
        params_file_arg,
        controller_server,
        planner_server,
        bt_navigator,
        behavior_server,
        waypoint_follower,
        lifecycle_manager,
    ])
