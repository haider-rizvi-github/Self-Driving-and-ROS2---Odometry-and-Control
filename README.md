# Self-Driving and ROS2: Odometry and Control

This repository contains my learning progress and project work for building a ROS2-based self-driving robot using Python, C++, odometry, control systems, and sensor fusion techniques such as Kalman Filters.

## Project Overview

In this project, we will create and simulate a self-driving robot using ROS2, Gazebo, Arduino, and robotics control libraries. The goal is to understand how real autonomous robots perceive, localize, and control their movement.

## What We Will Cover

* Create a real self-driving robot
* Master ROS2, the latest version of the Robot Operating System
* Implement sensor fusion algorithms
* Simulate a self-driving robot in Gazebo
* Program Arduino for robotics applications
* Use the `ros2_control` library
* Develop robot controllers
* Understand odometry and localization
* Learn Kalman Filters and Extended Kalman Filters
* Study probability theory for robotics
* Understand differential kinematics
* Create a digital twin of a self-driving robot
* Master the TF2 library

## Environment

* Ubuntu 24.04.3 LTS (Noble)
* ROS2 Jazzy
* Python 3 
* C++
* Gazebo
* Arduino
* ros2_control
* TF2
* Kalman Filters
* Extended Kalman Filter

## Installation Requirements

Before installing the required packages, update your system:

```bash
sudo apt update
sudo apt upgrade -y
```

### Install ROS2 Control, Controllers, Xacro, and Gazebo Packages

```bash
sudo apt install -y \
  ros-jazzy-ros2-control \
  ros-jazzy-ros2-controllers \
  ros-jazzy-xacro \
  ros-jazzy-ros-gz \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-joint-state-publisher-gui
```

### Install Additional ROS2 Packages

```bash
sudo apt install -y \
  ros-jazzy-tf-transformations \
  ros-jazzy-joy-teleop \
  ros-jazzy-joy \
  ros-jazzy-robot-localization \
  ros-jazzy-urdf.tutorial
```

### Visualizing URDF

To visualize the robot URDF model, run:

```bash
ros2 launch urdf_tutorial display.launch.py model:=/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-Control/src/robot_description/urdf/bumperbot.urdf.xacro
```

### Install Python Packages

```bash
sudo apt install -y python3-pip
pip install transforms3d
```

### Source ROS2 Jazzy

Run this command before working with ROS2:

```bash
source /opt/ros/jazzy/setup.bash
```

To source ROS2 automatically every time you open a new terminal, add it to `.bashrc`:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verify Installation

Check your ROS2 distribution:

```bash
printenv ROS_DISTRO
```

Expected output:

```bash
jazzy
```

Check if Gazebo integration is available:

```bash
ros2 pkg list | grep ros_gz
```

Check if ROS2 control packages are available:

```bash
ros2 pkg list | grep controller
```

## Differential-Drive Forward Kinematics

The relationship between robot velocity and wheel velocity is:

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

where:

- $V$ is the robot's linear velocity.
- $\omega$ is the robot's angular velocity.
- $r$ is the wheel radius.
- $s$ is the wheel separation.
- $\dot{\phi}_r$ is the right-wheel angular velocity.
- $\dot{\phi}_l$ is the left-wheel angular velocity.

## Bumperbot Controller Launch Instructions

To run the simulated Bumperbot with the controller, use the following launch sequence.

1. Launch the robot description in Gazebo:

```bash
ros2 launch robot_description gazebo.launch.py
```

2. Launch the bumperbot controller:

```bash
ros2 launch bumperbot_controller controller.launch.py
```

3. Send velocity commands to the controller:

```bash
ros2 topic pub /simple_velocity_controller/commands std_msgs/msg/Float64MultiArray 'layout:
  dim: []
  data_offset: 0
 data: [1,-1]
'
```

Command values:

* `1` = rotate the wheel forward
* `0` = stop the wheel
* `-1` = rotate the wheel backward

### Helpful ROS2 Control Commands

Use these commands to inspect the ROS2 control system and active controllers:

* `ros2 topic list`
* `ros2 control list_hardware_interfaces`
* `ros2 control list_hardware_components`
* `ros2 control list_controllers`

