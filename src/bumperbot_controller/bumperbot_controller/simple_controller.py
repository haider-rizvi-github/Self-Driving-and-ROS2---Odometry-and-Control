#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TwistStamped
import numpy as np


class SimpleController(Node):
    def __init__(self):
        super().__init__("simple_controller")

        self.get_logger().info("Simple Controller Node has been started.")

        # We derived a Differential Drive Kinematics model: Check the equation
        self.declare_parameter(
            "wheel_radius", 0.033
        )  # We can check the radius in the URDF file
        self.declare_parameter(
            "wheel_separation", 0.17
        )  # We can check the separation in the URDF file

        self.wheel_radius = (
            self.get_parameter("wheel_radius").get_parameter_value().double_value
        )
        self.wheel_separation = (
            self.get_parameter("wheel_separation").get_parameter_value().double_value
        )

        # Printing the parameters to the console
        self.get_logger().info("Using wheel radius %f" % self.wheel_radius)
        self.get_logger().info("Using wheel separation %f" % self.wheel_separation)

        # Create a publisher object to publish the wheel velocities
        self.wheel_cmd_pub_ = self.create_publisher(
            Float64MultiArray, "simple_velocity_controller/commands", 10
        )

        # Create a subscriber object to subscribe the commands coming from the joystick
        self.vel_sub_ = self.create_subscription(
            TwistStamped, "bumperbot_controller/cmd_vel", self.velCallback, 10
        )

        # Matrices to convert from linear and angular velocity to wheel velocities
        self.speed_conversion_ = np.array(
            [
                [self.wheel_radius / 2, self.wheel_radius / 2],
                [
                    self.wheel_radius / self.wheel_separation,
                    -self.wheel_radius / self.wheel_separation,
                ],
            ]
        )

        self.get_logger().info("The conversion matrix is: %s" % self.speed_conversion_)

    def velCallback(self, msg):
        robot_speed = np.array([[msg.twist.linear.x], [msg.twist.angular.z]])

        # taking inverse of the speed conversion matrix to get the wheel speeds
        wheel_speed = np.matmul(np.linalg.inv(self.speed_conversion_), robot_speed)
        wheel_speed_msg = Float64MultiArray()
        wheel_speed_msg.data = [
            wheel_speed[1, 0],
            wheel_speed[0, 0],
        ]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SimpleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
