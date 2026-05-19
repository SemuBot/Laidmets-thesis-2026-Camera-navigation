# Semubot Camera Navigation

ROS2 based autonomous navigation for **Semubot** using an Intel RealSense depth camera. The system supports Gazebo Harmonic simulation as well as real-robot deployment, and provides two SLAM backends (RTAB-Map and slam_toolbox) together with a Nav2 autonomous navigation stack.

## Packages

All packages live inside `semubot_ros2_ws/src/`.

| Package | Description |
|---------|-------------|
| [`semubot_description`](https://github.com/SemuBot/semubot_description) | URDF model with RealSense camera |
| `semubot_bringup` | Launch files for real SemuBot deployment |
| `semubot_camera_navigation` | SLAM (RTAB-Map / slam_toolbox), Nav2 |
| [`semubot_gazebo`](https://github.com/SemuBot/semubot_gazebo) | Gazebo Harmonic simulation with ros_gz bridges |

## Dependencies

- ROS2 Jazzy
- `realsense2_camera`, `realsense2_description`
- `rtabmap_launch`, `slam_toolbox`
- `nav2_controller`, `nav2_planner`, `nav2_bt_navigator`, `nav2_behaviors`, `nav2_lifecycle_manager`
- `robot_localization` (EKF)
- `depthimage_to_laserscan`
- `ros_gz_sim`, `ros_gz_bridge` (simulation only)

## Installation

### 1. Install ROS2 Jazzy

Follow the official guide:
https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

```bash
source /opt/ros/jazzy/setup.bash
```

### 2. Build the workspace

```bash
cd semubot_ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## Running the System

### Visualize the robot model

```bash
ros2 launch semubot_description display_robot.launch.py
```

### Gazebo simulation

```bash
# Empty world (default)
ros2 launch semubot_gazebo gazebo.launch.py

# Maze world
ros2 launch semubot_gazebo gazebo.launch.py world:=maze.sdf
```

Then in a separate terminal launch SLAM:

```bash
# RTAB-Map (default)
ros2 launch semubot_camera_navigation slam_bringup.launch.py use_sim_time:=true

# slam_toolbox
ros2 launch semubot_camera_navigation slam_bringup.launch.py use_sim_time:=true slam:=toolbox
```

Optionally add Nav2 in a third terminal:

```bash
ros2 launch semubot_camera_navigation nav2_bringup.launch.py use_sim_time:=true
```

### Real robot

**On the robot** - starts robot state publisher, RealSense camera, SLAM and optionally Nav2:

```bash
# RTAB-Map SLAM (default)
ros2 launch semubot_bringup robot_bringup.launch.py

# slam_toolbox instead of RTAB-Map
ros2 launch semubot_bringup robot_bringup.launch.py slam:=toolbox

# RTAB-Map + Nav2 autonomous navigation
ros2 launch semubot_bringup robot_bringup.launch.py nav:=true
```

**On the laptop** — starts RViz2 for monitoring:

```bash
ros2 launch semubot_bringup laptop_bringup.launch.py
```

## Author

Anton Laidmets  
University of Tartu - Computer Engineering  
Email: anton.laidmets@ut.ee
