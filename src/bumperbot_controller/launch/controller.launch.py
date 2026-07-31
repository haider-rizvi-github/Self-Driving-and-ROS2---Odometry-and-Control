from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    # creating path to the robot urdf file
    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(
                    get_package_share_directory("robot_description"),
                    "urdf",
                    "bumperbot.urdf.xacro",
                ),
            ]
        ),
        value_type=str,  # Specify the type of the parameter value
    )

    # Add the robot_state_publisher node
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",  # name of the executable
        parameters=[
            {"robot_description": robot_description},
            # {"use_sim_time": LaunchConfiguration("use_sim_time")},
        ],
    )  # not including node in node list to avoid duplication

    # Add the controller_manager node and give it the robot_description parameter and the path to the bumperbot_controllers.yaml file
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description},
            os.path.join(
                get_package_share_directory("bumperbot_controller"),
                "config",
                "bumperbot_controllers.yaml",
            ),
        ],
        output="screen",
    )

    # Spawn the joint_state_broadcaster controller
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    # spawn the aram_controller Node
    simple_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "simple_velocity_controller",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    return LaunchDescription(
        [
            # add the nodes to the launch description
            # controller_manager,
            joint_state_broadcaster_spawner,
            simple_controller,
        ]
    )
