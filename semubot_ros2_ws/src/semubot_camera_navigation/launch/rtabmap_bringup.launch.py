from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='false')
    use_sim_time = LaunchConfiguration('use_sim_time')

    rtabmap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('rtabmap_launch'),
                'launch',
                'rtabmap.launch.py'
            )
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'namespace': '',
            'frame_id': 'base_link',
            'odom_frame_id': 'odom',
            'visual_odometry': 'true',
            'subscribe_scan': 'true',
            'subscribe_scan_cloud': 'false',
            'subscribe_imu': 'false',
            'imu_topic': '/camera/imu',
            'approx_sync': 'true',
            'wait_for_transform': '1.0',
            'qos': '1',
            'rgb_topic': '/camera/color/image_raw',
            'depth_topic': '/camera/aligned_depth_to_color/image_raw',
            'camera_info_topic': '/camera/color/camera_info',
            'odom_topic': '/odom',
            'publish_tf': 'true',
            'odom_args': '--Vis/MinInliers 10 --OdomF2M/MaxSize 1000 --Odom/ResetCountdown 15',
            'rtabmap_viz': 'false',
            'rviz': 'false',
            'log_level': 'error',

            #'localization': 'true', # Uncomment when you have the map and just want to localize

            'delete_db_on_start': 'true',
            'args': '--verbosity 1 '
                    '--Reg/Force3DoF true '
                    '--RGBD/CreateOccupancyGrid true '
                    '--Grid/Sensor 1 --Grid/3D true '
                    '--Grid/RangeMax 5.0 --Grid/RayTracing true '
                    '--Grid/NoiseFilteringRadius 0.1 --Grid/NoiseFilteringMinNeighbors 5 '
                    '--cloud_voxel_size 0.05 '
                    '--Rtabmap/DetectionRate 1 '
                    '--Mem/ImagePreDecimation 2 '
                    '--Mem/DepthCompressionFormat .png '
                    '--Kp/MaxFeatures 200 '
                    '--Mem/STMSize 30 '
        }.items()
    )

    return LaunchDescription([
        use_sim_time_arg,
        rtabmap,
    ])
