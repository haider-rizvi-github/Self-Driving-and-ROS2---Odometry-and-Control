#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import JointState
import numpy as np
from rclpy.time import Time
from rclpy.constants import S_TO_NS # seconds to nanoseconds
from nav_msgs.msg import Odometry
from tf_transformations import quaternion_from_euler
import math


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

        # For Odometry
        self.left_wheel_prev_pos_ = None
        self.right_wheel_prev_pos_ = None
        self.prev_time_ = None        #self.get_clock().now()  # holds the value of current moment of time

        # position of robot
        self.x_ = 0.0
        self.y_ = 0.0
        self.theta = 0.0

        # hint: (first:msg type, second: "Topic name of our choice", third: time)
        # Create a publisher object to publish the wheel velocities
        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray, "simple_velocity_controller/commands", 10)

        #Creating a publisher object for odom
        self.odom_pub = self.create_publisher(Odometry, "bumperbot_controller/odom", 10)

        # Create a subscriber object to subscribe the commands coming from the joystick
        self.vel_sub_ = self.create_subscription(TwistStamped, "bumperbot_controller/cmd_vel", self.velCallback, 10)

        # Create a new subscriber to hold encoder values from gazebo  
        self.joint_sub_ = self.create_subscription(JointState, "joint_states", self.jointCallback, 10)

        # Matrices to convert from linear and angular velocity to wheel velocities
        self.speed_conversion_ = np.array([[self.wheel_radius / 2, self.wheel_radius / 2],
                                           [self.wheel_radius / self.wheel_separation,-self.wheel_radius / self.wheel_separation],])

        self.odom_msg_ = Odometry()
        self.odom_msg_.header.frame_id = "odom"
        self.odom_msg_.child_frame_id = "base_footprint"  # first link of the robot to which the odom will be attached
        self.odom_msg_.pose.pose.orientation.x = 0.0
        self.odom_msg_.pose.pose.orientation.y = 0.0
        self.odom_msg_.pose.pose.orientation.z = 0.0
        self.odom_msg_.pose.pose.orientation.w = 1.0

        self.get_logger().info("The conversion matrix is: %s" % self.speed_conversion_)

    def velCallback(self, msg):
        robot_speed = np.array([[msg.twist.linear.x],
                                [msg.twist.angular.z]])

        # taking inverse of the speed conversion matrix to get the wheel speeds
        wheel_speed = np.matmul(np.linalg.inv(self.speed_conversion_), robot_speed)
        wheel_speed_msg = Float64MultiArray()
        wheel_speed_msg.data = [
            wheel_speed[1, 0],
            wheel_speed[0, 0],
        ]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

    def jointCallback(self, msg):
        if len(msg.position) < 2:
            self.get_logger().warning(
                "JointState message does not contain both wheel positions."
            )
            return

        current_time = Time.from_msg(msg.header.stamp)
        left_position = msg.position[1]
        right_position = msg.position[0]

        # Use the first message only to initialize odometry.
        if self.prev_time_ is None:
            self.left_wheel_prev_pos_ = left_position
            self.right_wheel_prev_pos_ = right_position
            self.prev_time_ = current_time
            return

        dt_nanoseconds = (current_time - self.prev_time_).nanoseconds

        # Prevent division by zero or invalid negative time.
        if dt_nanoseconds <= 0:
            self.get_logger().warning(
                "Ignoring joint state because dt is zero or negative."
            )
            return

        dt_seconds = dt_nanoseconds / S_TO_NS

        dp_left = left_position - self.left_wheel_prev_pos_
        dp_right = right_position - self.right_wheel_prev_pos_

        fi_left = dp_left / dt_seconds
        fi_right = dp_right / dt_seconds

        linear = self.wheel_radius * (fi_right + fi_left) / 2.0
        angular = (self.wheel_radius * (fi_right - fi_left)/ self.wheel_separation)
        d_s= (self.wheel_radius * dp_right + self.wheel_radius * dp_left) /2.0            # position
        d_theta = (self.wheel_radius * dp_right - self.wheel_radius * dp_left) / self.wheel_separation   # orientation
        

        # Update previous values only after a valid calculation.
        self.left_wheel_prev_pos_ = left_position
        self.right_wheel_prev_pos_ = right_position
        self.prev_time_ = current_time
        self.theta += d_theta   
        self.x_ += d_s * math.cos(self.theta)
        self.y_ += d_s * math.sin(self.theta)        

        #updating odometry msg
        q = quaternion_from_euler(0,0,self.theta)
        self.odom_msg_.pose.pose.orientation.x =q[0]
        self.odom_msg_.pose.pose.orientation.y =q[1]
        self.odom_msg_.pose.pose.orientation.z =q[2]
        self.odom_msg_.pose.pose.orientation.w =q[3]
        self.odom_msg_.header.stamp = self.get_clock().now().to_msg()
        self.odom_msg_.pose.pose.position.x = self.x_
        self.odom_msg_.pose.pose.position.y = self.y_
        self.odom_msg_.twist.twist.linear.x = linear
        self.odom_msg_.twist.twist.angular.z = angular

        self.odom_pub.publish(self.odom_msg_)

        self.get_logger().info("Linear Velocity: %f  ,Angular Velocity: %f" % (linear, angular))
        self.get_logger().info("x: %f, y: %f, Theta: %f" % (self.x_, self.y_, self.theta))

        


def main(args=None):
    rclpy.init(args=args)
    node = SimpleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
