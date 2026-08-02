from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument

import os


def generate_launch_description():

    use_python_arg = DeclareLaunchArgument(
        "use_python",
        default_value="true",
        description="Whether to use the Python launch file or not",
    )

    # Can be changed depending on the robot's wheel radius and separation between the wheels.
    # These values are used in the controller configuration file to calculate the robot's odometry.
    wheel_radius_arg = DeclareLaunchArgument(
        "wheel_radius",
        default_value="0.033",
        description="Radius of the wheels in meters",
    )

    wheel_separation_arg = DeclareLaunchArgument(
        "wheel_separation",
        default_value="0.17",
        description="Separation between the wheels in meters",
    )

    use_python = LaunchConfiguration("use_python")
    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")

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

    simple_controller_py = Node(
        package="bumperbot_controller",
        executable="simple_controller",
        name="simple_controller",
        output="screen",
        parameters=[
            {"wheel_radius": wheel_radius, "wheel_separation": wheel_separation}
        ],
    )

    return LaunchDescription(
        [
            # add the nodes to the launch description
            # controller_manager,
            use_python_arg,
            wheel_radius_arg,
            wheel_separation_arg,
            joint_state_broadcaster_spawner,
            simple_controller,
            simple_controller_py,
        ]
    )
