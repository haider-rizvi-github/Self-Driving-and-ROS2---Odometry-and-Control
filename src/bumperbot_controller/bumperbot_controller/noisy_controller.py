#!/usr/bin/env python3

'''
    This is an updated controller of a simple_controller.py as the noise is added into it. 
    This helps us to depicts the real sensor output data  
'''

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import  TransformStamped
from tf2_ros import TransformBroadcaster
from sensor_msgs.msg import JointState
import numpy as np
from rclpy.time import Time
from rclpy.constants import S_TO_NS # seconds to nanoseconds
from nav_msgs.msg import Odometry
from tf_transformations import quaternion_from_euler
import math


class NoisyController(Node):
    def __init__(self):
        super().__init__("noisy_controller")

        self.get_logger().info("Noisy Controller Node has been started.")

        self.tf_broadcaster_ = TransformBroadcaster(self)  # to update frame to Odom

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

        #Creating a publisher object for odom
        self.odom_pub = self.create_publisher(Odometry, "bumperbot_controller/odom_noisy", 10)

        # Create a new subscriber to hold encoder values from gazebo  
        self.joint_sub_ = self.create_subscription(JointState, "joint_states", self.jointCallback, 10)

        self.odom_msg_ = Odometry()
        self.odom_msg_.header.frame_id = "odom"
        self.odom_msg_.child_frame_id = "base_footprint_ekf"  # first link of the robot to which the odom will be attached
        self.odom_msg_.pose.pose.orientation.x = 0.0
        self.odom_msg_.pose.pose.orientation.y = 0.0
        self.odom_msg_.pose.pose.orientation.z = 0.0
        self.odom_msg_.pose.pose.orientation.w = 1.0


    def jointCallback(self, msg):
        if len(msg.position) < 2:
            self.get_logger().warning(
                "JointState message does not contain both wheel positions."
            )
            return

        # for noisy: adding wheel_encoder_left and right
        wheel_encoder_left= msg.position[1] + np.random.normal(0, 0.005)
        wheel_encoder_right= msg.position[0] + np.random.normal(0, 0.005)   
        
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

        # using noisy positions in dp_left and dp_right instead of the absolute values which
        # we are getting from left_position and right position variables

        dp_left = wheel_encoder_left - self.left_wheel_prev_pos_
        dp_right = wheel_encoder_right - self.right_wheel_prev_pos_

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
        # Convert yaw angle to quaternion.
        q = quaternion_from_euler(0.0, 0.0, self.theta)

        current_stamp = self.get_clock().now().to_msg()

        # Update odometry message.
        self.odom_msg_.header.stamp = current_stamp

        self.odom_msg_.pose.pose.position.x = self.x_
        self.odom_msg_.pose.pose.position.y = self.y_
        self.odom_msg_.pose.pose.position.z = 0.0

        self.odom_msg_.pose.pose.orientation.x = q[0]
        self.odom_msg_.pose.pose.orientation.y = q[1]
        self.odom_msg_.pose.pose.orientation.z = q[2]
        self.odom_msg_.pose.pose.orientation.w = q[3]

        self.odom_msg_.twist.twist.linear.x = linear
        self.odom_msg_.twist.twist.angular.z = angular

        self.odom_pub.publish(self.odom_msg_)

        # Broadcast the dynamic TF: odom -> base_footprint.
        odom_transform = TransformStamped()

        odom_transform.header.stamp = current_stamp
        odom_transform.header.frame_id = "odom"
        odom_transform.child_frame_id = "base_footprint_noisy"

        odom_transform.transform.translation.x = self.x_
        odom_transform.transform.translation.y = self.y_
        odom_transform.transform.translation.z = 0.0

        odom_transform.transform.rotation.x = q[0]
        odom_transform.transform.rotation.y = q[1]
        odom_transform.transform.rotation.z = q[2]
        odom_transform.transform.rotation.w = q[3]

        self.tf_broadcaster_.sendTransform(odom_transform)

        self.odom_pub.publish(self.odom_msg_)

        self.get_logger().info("Linear Velocity: %f  ,Angular Velocity: %f" % (linear, angular))
        self.get_logger().info("x: %f, y: %f, Theta: %f" % (self.x_, self.y_, self.theta))

        


def main(args=None):
    rclpy.init(args=args)
    node = NoisyController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
