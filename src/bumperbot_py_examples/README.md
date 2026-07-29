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

## Gazebo launch

This workspace includes the robot description package for Gazebo.

```bash
ros2 launch robot_description gazebo.launch.py
```
