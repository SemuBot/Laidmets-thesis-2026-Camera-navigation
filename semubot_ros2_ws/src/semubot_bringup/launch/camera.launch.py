from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    realsense = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('realsense2_camera'),
                'launch',
                'rs_launch.py'
            )
        ),
        launch_arguments={
            'camera_name': 'camera',
            'camera_namespace': '',
            'enable_depth': 'true',
            'enable_color': 'true',
            'enable_gyro': 'true',
            'enable_accel': 'true',
            'unite_imu_method': '1',
            'depth_module.depth_profile': '640x480x15',
            'rgb_camera.color_profile': '640x480x15',
            'pointcloud.enable': 'false',
            'align_depth.enable': 'true',
            'initial_reset': 'true',
            'reconnect_timeout': '10.0',
        }.items()
    )

    return LaunchDescription([realsense])
