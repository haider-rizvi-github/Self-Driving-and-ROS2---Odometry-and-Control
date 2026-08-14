# Self-Driving and ROS 2: Odometry and Control

This repository documents my learning progress and project work on building a ROS 2-based self-driving robot using Python, C++, odometry, control systems, and sensor-fusion techniques such as Kalman Filters.

## Project Overview

This project focuses on creating and simulating a self-driving robot using ROS 2, Gazebo, Arduino, and robotics control libraries. The goal is to understand how autonomous robots perceive their surroundings, estimate their position, and control their movement.

## Topics Covered

- Building a real self-driving robot
- ROS 2 fundamentals
- Sensor-fusion algorithms
- Robot simulation in Gazebo
- Arduino programming for robotics
- The `ros2_control` framework
- Robot controller development
- Odometry and localization
- Kalman Filters and Extended Kalman Filters
- Probability theory for robotics
- Differential-drive kinematics
- Digital twins for robots
- The TF2 library
- Dynamic TF publication with quaternion rotation computed from Euler angles in `src/bumperbot_py_examples/bumperbot_py_examples/simple_dynamic_tf_kinematics.py`
- Odometry calculation in `src/bumperbot_controller/bumperbot_controller/simple_controller.py` using differential-drive equations:
  - linear displacement: `d_s = (r * Δφ_r + r * Δφ_l) / 2`
  - orientation change: `d_θ = (r * Δφ_r - r * Δφ_l) / wheel_separation`
  - pose update: `x += d_s * cos(θ)` and `y += d_s * sin(θ)`

## Environment

- Ubuntu 24.04.3 LTS (Noble)
- ROS 2 Jazzy
- Gazebo Harmonic
- Python 3
- C++
- Arduino
- `ros2_control`
- TF2
- Kalman Filter
- Extended Kalman Filter

## Installation Requirements

### Update the System

Before installing the required packages, update the system:

```bash
sudo apt update
sudo apt upgrade -y
```

### Install ROS 2 Control and Gazebo Packages

```bash
sudo apt install -y \
  ros-jazzy-ros2-control \
  ros-jazzy-ros2-controllers \
  ros-jazzy-xacro \
  ros-jazzy-ros-gz \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-joint-state-publisher-gui
```

### Install Additional ROS 2 Packages

```bash
sudo apt install -y \
  ros-jazzy-tf-transformations \
  ros-jazzy-joy-teleop \
  ros-jazzy-joy \
  ros-jazzy-robot-localization \
  ros-jazzy-urdf-tutorial \
  python3-transforms3d
```

### Install Plotjuggler

Plotjuggler is used to visualize real-time topic values as plotted graphs.

```bash
sudo apt-get install ros-jazzy-plotjuggler
sudo apt install ros-${ROS_DISTRO}-plotjuggler-ros
```

## Source ROS 2 Jazzy

Run the following command before working with ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

To source ROS 2 automatically whenever a new terminal is opened:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Build the Workspace

Run these commands from the root of the ROS 2 workspace:

```bash
colcon build --symlink-install
source install/setup.bash
```

After making changes to a package, rebuild the workspace and source it again:

```bash
colcon build --symlink-install
source install/setup.bash
```

## Verify the Installation

Check the active ROS 2 distribution:

```bash
printenv ROS_DISTRO
```

Expected output:

```text
jazzy
```

Check whether the Gazebo integration packages are available:

```bash
ros2 pkg list | grep ros_gz
```

Check whether ROS 2 controller packages are available:

```bash
ros2 pkg list | grep controller
```

## Visualize the URDF Model

From the workspace root, run:

```bash
ros2 launch urdf_tutorial display.launch.py \
  model:="$(pwd)/src/robot_description/urdf/bumperbot.urdf.xacro"
```

This opens RViz and displays the Bumperbot URDF model.

<!--
## Differential-Drive Forward Kinematics

The relationship between the robot velocity and wheel angular velocities is:

```math
\begin{bmatrix}
V \\
\omega
\end{bmatrix}
=
\begin{bmatrix}
\frac{r}{2} & \frac{r}{2} \\
\frac{r}{s} & -\frac{r}{s}
\end{bmatrix}
\begin{bmatrix}
\dot{\phi}_r \\
\dot{\phi}_l
\end{bmatrix}
```

where:

- $V$ is the robot's linear velocity in metres per second.
- $\omega$ is the robot's angular velocity in radians per second.
- $r$ is the wheel radius in metres.
- $s$ is the wheel separation or track width, measured between the left and right wheel contact points.
- $\dot{\phi}_r$ is the right-wheel angular velocity in radians per second.
- $\dot{\phi}_l$ is the left-wheel angular velocity in radians per second.

The corresponding scalar equations are:

```math
V = \frac{r}{2}\left(\dot{\phi}_r+\dot{\phi}_l\right)
```

```math
\omega = \frac{r}{s}\left(\dot{\phi}_r-\dot{\phi}_l\right)
```
-->

## Bumperbot Controller Launch Instructions

Open separate terminals for the robot simulation, controller, and velocity commands. Source the workspace in every terminal:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

### 1. Launch the Robot in Gazebo

```bash
ros2 launch robot_description gazebo.launch.py
```

### 2. Launch a Controller

The launch file supports two controller options:

- Launch the simple velocity controller:

```bash
ros2 launch bumperbot_controller controller.launch.py use_simple_controller:=true
```

- Launch the bumperbot_controller that uses the diff_drive_controller library:

```bash
ros2 launch bumperbot_controller controller.launch.py use_simple_controller:=false
```

To view the odometry messages published by the controller, run the following in a separate terminal:

```bash
ros2 topic echo /bumperbot_controller/odom --no-arr
```

### 3. Move the Robot with Joystick

If you want to control the robot with a joystick, run the following in a third terminal after connecting the controller:

```bash
ros2 launch bumperbot_controller joystick_teleop.launch.py
```

Tip: connect the controller first, and only then run the command.

Run the Trajectory_Drawing node

To publish the recorded trajectory (Path) for visualization, run the trajectory drawing node in a separate terminal:

```bash
ros2 run Draw_trajectory trajectory_drawer
```

Visualize the trajectory in RViz2

To view the trajectory in RViz2:

1. Start RViz2:

```bash
rviz2
```

2. In RViz2, set the Fixed Frame to "odom" (top-left under Global Options).
3. Add a "Path" display (click the Add button) and set its Topic to `/bumperbot_controller/trajectory` (the node publishes the Path here).

This will show the recorded trajectory as a line of poses in the odom frame.


## Robot Visualization of Odometry and Control

Use the following workflow to launch the robot, controller, joystick, RViz, and PlotJuggler for real-time visualization of odometry and control signals.

### Launch Gazebo

```bash
ros2 launch robot_description gazebo.launch.py
```

### Launch the Controller

You can switch between the simple controller and the diff-drive controller by using the launch file options.

```bash
ros2 launch bumperbot_controller controller.launch.py
```

### Launch the Joystick Controller

```bash
ros2 launch bumperbot_controller joystick_teleop.launch.py
```

### Launch RViz2

```bash
rviz2
```

### Launch PlotJuggler

PlotJuggler is useful for visualizing real-time topic data and comparing the effects of noise on the robot signals.

```bash
ros2 run plotjuggler plotjuggler
```

### Visualize the Signals in PlotJuggler

1. Set up the topic subscribers in PlotJuggler.
2. Drag out the signals you want to compare, such as odometry values, wheel speeds, or control inputs.
3. Inspect the plotted graphs to analyze signal behavior and noise effects.

### 4. Move the Robot with the Controller

To drive the robot using the controller launch file, publish a TwistStamped message to the `/bumperbot_controller/cmd_vel` topic:

```bash
ros2 topic pub /bumperbot_controller/cmd_vel geometry_msgs/msg/TwistStamped '
header:
  stamp:
    sec: 0
    nanosec: 0
  frame_id: ""
twist:
  linear:
    x: 0.2
    y: 0.0
    z: 0.0
  angular:
    x: 0.0
    y: 0.0
    z: -0.5
'
```

### 5. Send Wheel-Velocity Commands

In a third terminal, publish wheel velocities:

```bash
ros2 topic pub --once \
  /simple_velocity_controller/commands \
  std_msgs/msg/Float64MultiArray \
  "{data: [1.0, -1.0]}"
```

The two values represent the commanded angular velocities of the two wheel joints. Their order depends on the joint order defined in the controller configuration.

Example commands:

### Move the Wheels in the Same Direction

```bash
ros2 topic pub --once \
  /simple_velocity_controller/commands \
  std_msgs/msg/Float64MultiArray \
  "{data: [1.0, 1.0]}"
```

### Move the Wheels in Opposite Directions

```bash
ros2 topic pub --once \
  /simple_velocity_controller/commands \
  std_msgs/msg/Float64MultiArray \
  "{data: [1.0, -1.0]}"
```

### Stop Both Wheels

```bash
ros2 topic pub --once \
  /simple_velocity_controller/commands \
  std_msgs/msg/Float64MultiArray \
  "{data: [0.0, 0.0]}"
```

> Depending on the wheel-joint axis definitions, the signs required for straight or rotational motion may be reversed.

## Helpful ROS 2 Control Commands

List available ROS 2 topics:

```bash
ros2 topic list
```

List the available hardware interfaces:

```bash
ros2 control list_hardware_interfaces
```

List the hardware components:

```bash
ros2 control list_hardware_components
```

List the loaded controllers:

```bash
ros2 control list_controllers
```

Check information about the velocity-command topic:

```bash
ros2 topic info /simple_velocity_controller/commands
```

## IMU (Inertial Measurement Unit)

An IMU sensor has been added to the robot model and simulation. The IMU provides accelerometer and gyroscope measurements which are used to improve odometry, state estimation, and sensor-fusion experiments (for example, Kalman Filters and Extended Kalman Filters). In the Gazebo simulation the IMU data is published as a standard ROS 2 Imu message (sensor_msgs/msg/Imu), typically on the /imu/data topic.

Key notes and usage:

- Topic: /imu/data (sensor_msgs/msg/Imu)
- Frames: imu_link -> base_link (verify in the TF tree)
- Purpose: fuse wheel odometry and IMU measurements to obtain more robust pose and orientation estimates, particularly during wheel slip or when wheel encoder data is noisy.
- Filtering: use robot_localization (ekf_localization_node) or custom filter nodes to combine odometry and IMU in a consistent state-estimation pipeline.
- Simulation noise: configure realistic noise parameters in the Gazebo sensor plugin, or model noise in software when testing filters.

To enable or configure the IMU in this workspace, check and edit the robot URDF/XACRO and Gazebo launch files:

- Robot URDF/XACRO: [src/robot_description/urdf/bumperbot.urdf.xacro](/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-Control/src/robot_description/urdf/bumperbot.urdf.xacro)
- Gazebo launch: [src/robot_description/launch/gazebo.launch.py](/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-Control/src/robot_description/launch/gazebo.launch.py)

## Repository Purpose

This repository is intended for learning and experimentation with mobile-robot kinematics, ROS 2 control, Gazebo simulation, odometry, localization, and sensor fusion.