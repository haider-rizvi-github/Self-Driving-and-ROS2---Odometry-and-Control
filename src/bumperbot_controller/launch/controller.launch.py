#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():


    # Launch arguments

    wheel_radius_arg = DeclareLaunchArgument(
        "wheel_radius",
        default_value="0.033",
        description="Radius of each wheel in metres",
    )

    wheel_separation_arg = DeclareLaunchArgument(
        "wheel_separation",
        default_value="0.17",
        description="Distance between the left and right wheels in metres",
    )

    use_simple_controller_arg = DeclareLaunchArgument(
        "use_simple_controller",
        default_value="true",
        description=(
            "Use the custom simple velocity controller when true; "
            "use diff_drive_controller when false"
        ),
    )

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use the Gazebo simulation clock",
    )


    # Launch configurations


    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")
    use_simple_controller = LaunchConfiguration("use_simple_controller")
    use_sim_time = LaunchConfiguration("use_sim_time")


    # Robot description


    xacro_file = os.path.join(
        get_package_share_directory("robot_description"),
        "urdf",
        "bumperbot.urdf.xacro",
    )

    robot_description = ParameterValue(
        Command(["xacro ", xacro_file]),
        value_type=str,
    )


    # Robot State Publisher


    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": ParameterValue(
                    use_sim_time,
                    value_type=bool,
                ),
            }
        ],
    )

    # Joint State Broadcaster


    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="spawner_joint_state_broadcaster",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )


    # Standard ROS 2 differential-drive controller
    # Starts only when use_simple_controller is false.

    diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="spawner_bumperbot_controller",
        output="screen",
        arguments=[
            "bumperbot_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        condition=UnlessCondition(use_simple_controller),
    )

    # Custom simple controller
    # Starts only when use_simple_controller is true.


    simple_controller_group = GroupAction(
        condition=IfCondition(use_simple_controller),
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                name="spawner_simple_velocity_controller",
                output="screen",
                arguments=[
                    "simple_velocity_controller",
                    "--controller-manager",
                    "/controller_manager",
                ],
            ),
            Node(
                package="bumperbot_controller",
                executable="simple_controller",
                name="simple_controller",
                output="screen",
                parameters=[
                    {
                        "wheel_radius": ParameterValue(
                            wheel_radius,
                            value_type=float,
                        ),
                        "wheel_separation": ParameterValue(
                            wheel_separation,
                            value_type=float,
                        ),
                        "use_sim_time": ParameterValue(
                            use_sim_time,
                            value_type=bool,
                        ),
                    }
                ],
            ),
        ],
    )


    return LaunchDescription(
        [
            wheel_radius_arg,
            wheel_separation_arg,
            use_simple_controller_arg,
            use_sim_time_arg,
            robot_state_publisher,
            joint_state_broadcaster_spawner,
            diff_drive_controller_spawner,
            simple_controller_group,
        ]
    )