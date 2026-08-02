from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # This node is simple a Ros2 driver which reads input from a joystick device and publishes it as a ROS2 topic.
    # The joy_node is configured using the joy_config.yaml file, which specifies the joystick device and other parameters.
    joy_node = Node(
        package="joy",
        executable="joy_node",
        name="joystick",
        parameters=[
            os.path.join(
                get_package_share_directory("bumperbot_controller"),
                "config",
                "joy_config.yaml",
            )
        ],
        # description="Joystick node to read input from a joystick device",
    )

    # This node subscribes to the joystick topic published by the joy_node and converts the joystick input into robot commands.
    joy_teleop_node = Node(
        package="joy_teleop",
        executable="joy_teleop",
        name="joy_teleop",
        parameters=[
            os.path.join(
                get_package_share_directory("bumperbot_controller"),
                "config",
                "joy_teleop.yaml",
            )
        ],
        # description="Node to convert joystick input to robot commands",
    )

    return LaunchDescription([joy_node, joy_teleop_node])
