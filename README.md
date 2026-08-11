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

### 3. Move the Robot with Joystick

If you want to control the robot with a joystick, run the following in a third terminal after connecting the controller:

```bash
ros2 launch bumperbot_controller joystick_teleop.launch.py
```

Tip: connect the controller first, and only then run the command.

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

## Repository Purpose

This repository is intended for learning and experimentation with mobile-robot kinematics, ROS 2 control, Gazebo simulation, odometry, localization, and sensor fusion.