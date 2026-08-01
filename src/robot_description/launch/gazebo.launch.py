from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import (
    DeclareLaunchArgument,
    SetEnvironmentVariable,
    IncludeLaunchDescription,
)
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory
from pathlib import Path


def generate_launch_description():

    ros_distro = os.environ["ROS_DISTRO"]
    is_ignition = "true" if ros_distro == "humble" else "false"

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            get_package_share_directory("robot_description"),
            "urdf",
            "bumperbot.urdf.xacro",
        ),  # Path to default URDF file
        description="Absolute path to robot urdf file",
    )

    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[
            str(
                Path(get_package_share_directory("robot_description")).parent.resolve()
            ),
        ],
    )

    robot_description = ParameterValue(
        Command(
            ["xacro ", LaunchConfiguration("model"), " is_ignition:=", is_ignition]
        ),
        value_type=str,  # Specify the type of the parameter value
    )

    # Add the robot_state_publisher node
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",  # name of the executable
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            },  # use sim time for gazebo
        ],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("ros_gz_sim"),
                    "launch",
                ),
                "/gz_sim.launch.py",
            ]
        ),
        launch_arguments=[
            ("gz_args", ["-v 4 -r empty.sdf"]),
        ],
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-name",
            "bumperbot",
            "-topic",
            "robot_description",
            "-x",
            "0",
            "-y",
            "0",
            "-z",
            "0.01",
        ],
    )

    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/model/manipulator/joint_state@sensor_msgs/msg/JointState[gz.msgs.msg.ModelJointState",
            "/model/manipulator/pose@geometry_msgs/msg/PoseStamped[gz.msgs.msg.Pose",
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.msg.Clock",
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            model_arg,
            robot_state_publisher,
            gazebo_resource_path,
            gazebo,
            gz_spawn_entity,
            # gz_ros2_bridge,
        ]
    )
