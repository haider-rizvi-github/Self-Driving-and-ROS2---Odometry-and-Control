# bumperbot_py_examples

This package contains example ROS2 Python nodes for a bumperbot project. It includes a publisher node, a subscriber node, and a parameter node for learning how ROS2 Python nodes, topics, and parameters work.

## Package structure

- `package.xml`
  - ROS2 package manifest.
  - Declares package metadata, dependencies, and exports.

- `setup.py`
  - Python package setup script.
  - Registers console scripts for running nodes with `ros2 run`.

- `setup.cfg`
  - Optional metadata and configuration for packaging and linting.

- `resource/bumperbot_py_examples`
  - Marker file used by ROS2 package discovery.

- `bumperbot_py_examples/`
  - Python module directory containing example node implementations.
  - `publisher_member_function.py` – publisher node.
  - `subscriber_member_function.py` – subscriber node.
  - `simple_parameter.py` – node with declared parameters and parameter change validation.

- `test/`
  - Unit test files for package validation.
  - `test_copyright.py`, `test_flake8.py`, `test_pep257.py`.

## Example nodes

### Publisher

Runs a simple publisher that publishes `std_msgs/String` messages on the `topic` topic.

```bash
ros2 run bumperbot_py_examples publisher_member_function
```

### Subscriber

Runs a subscriber node that listens to `topic` and prints received messages.

```bash
ros2 run bumperbot_py_examples subscriber_member_function
```

### Parameter node

Runs a node that declares two parameters:
- `simple_int` (default: `42`)
- `simple_param_string` (default: `Haider`)

```bash
ros2 run bumperbot_py_examples simple_parameter
```

#### Get parameter values

```bash
ros2 param get /simple_parameter_node simple_int
ros2 param get /simple_parameter_node simple_param_string
```

#### Change parameter values

```bash
ros2 run bumperbot_py_examples simple_parameter --ros-args -p simple_param_string:="Ali"
ros2 run bumperbot_py_examples simple_parameter --ros-args -p simple_int:=30
```

## Service node example

Runs a service server node that handles the `/add_two_ints` service using `bumperbot_msgs/srv/AddTwoInts`.

To start the service node:

```bash
ros2 run bumperbot_py_examples simple_service_server
```

Then call the service from another terminal:

```bash
ros2 service call /add_two_ints bumperbot_msgs/srv/AddTwoInts "{a: 6, b: 5}"
```

## Service client example

Runs a client node that sends two integers to the `/add_two_ints` service and prints the sum response.

To run the client with arguments `5` and `4`:

```bash
ros2 run bumperbot_py_examples simple_service_client 5 4
```

## Turtlesim Kinematics Example

This package includes `turtlesim_kinematics.py`, which reads pose updates from two turtles in the `turtlesim` simulator and logs the translation vector from `turtle1` to `turtle2`.

To run the node, use these commands in separate terminals:

```bash
ros2 run turtlesim turtlesim_node
```

```bash
ros2 service call /spawn turtlesim/srv/Spawn "x: 1.0
y: 4.0
theta: 0.0
name: 'turtle2'"
```

```bash
ros2 run bumperbot_py_examples simple_turtlesim_kinematics
```

```bash
ros2 run turtlesim turtle_teleop_key
```

This starts `turtlesim`, spawns a second turtle named `turtle2`, runs the kinematics node, and enables keyboard teleoperation for turtle control.

## TF kinematics examples

These examples publish coordinate-frame relationships (TF transforms) so you can visualize the robot frames in RViz.

### Dynamic TF example

The node in `bumperbot_py_examples/simple_dynamic_tf_kinematics.py` publishes two transforms:

- a static transform from `bumperbot_base` to `bumperbot_top` (the top frame stays 0.3 m above the base)
- a dynamic transform from `odom` to `bumperbot_base` that slowly moves the base along the x-axis over time

This shows how a robot can have a fixed frame relationship for body parts and a changing frame relationship for motion.

To run it:

1. Open a terminal and start RViz:

   ```bash
   rviz2
   ```

2. In RViz, set the Fixed Frame to `odom` and add a `TF` display.

3. In another terminal, run:

   ```bash
   ros2 run bumperbot_py_examples simple_dynamic_tf_kinematics
   ```

### Static TF example

The node in `bumperbot_py_examples/simple_static_tf_kinematics.py` publishes a single static transform from `bumperbot_base` to `bumperbot_top`.

This is useful for showing a fixed relationship between two robot frames.

To run it:

1. Open a terminal and start RViz:

   ```bash
   rviz2
   ```

2. In RViz, set the Fixed Frame to `bumperbot_base` and add a `TF` display.

3. In another terminal, run:

   ```bash
   ros2 run bumperbot_py_examples simple_tf_kinematics
   ```

## Gazebo launch

This workspace includes the robot description package for Gazebo.

```bash
ros2 launch robot_description gazebo.launch.py
```
