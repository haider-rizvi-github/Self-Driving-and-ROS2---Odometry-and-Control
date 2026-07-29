# robot_description

This package contains the robot description assets for the ROS2 project. It is organized into standard ROS package files plus directories for URDF models, source code, meshes, and public C++ headers.

## Package structure

- `CMakeLists.txt`
  - Build instructions for the package.
  - Defines how the robot description package is configured and installed.

- `package.xml`
  - ROS package manifest.
  - Declares package dependencies, metadata, and package exports.

- `include/`
  - Public header files for the package.
  - Typically used for C++ code that needs to be exposed to other packages.

- `src/`
  - Source code for any nodes or utilities in this package.
  - Contains implementation files used by the package.

- `urdf/`
  - Contains the robot model definition files.
  - `bumperbot.urdf.xacro` is the XACRO source used to generate the robot URDF.
  - To visualize with the urdf_tutorial package use `ros2 launch urdf_tutorial display.launch.py model:=/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-Control/src/robot_description/urdf/bumperbot.urdf.xacro`
  - To launch Gazebo with this robot description use `ros2 launch robot_description gazebo.launch.py`

- `meshes/`
  - Geometry files used by the URDF models.
  - Stores mesh assets for visual and collision geometry.
