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
  ros-jazzy-robot-localization
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

