#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

class KalmanFilterNode(Node):
    def __init__(self):
        super().__init__('kalman_filter_node')
        self.get_logger().info('Kalman Filter Node has been started.')

        self.odom_sub = self.create_subscription( Odometry,"bumperbot_controller/odom_noisy", self.odomCallback, 10)
        self.imu_sub = self.create_subscription( Imu,"imu", self.imuCallback, 10)
        self.odom_pub = self.create_publisher(Odometry, "bumperbot_controller/odom_kalman_filtered", 10)

        # Initialize Kalman filter variables
        self.mean_ = 0.0
        self.variance_ = 1000.0

        self.imu_angular_z_ = 0.0  # This will store the last received angular velocity from the IMU
        self.is_first_odom_ = True  # Flag to check if it's the first odometry message
        self.last_angular_z_ = 0.0  # This will store the last angular velocity from the odometry

        self.motion_ = 0.0          # store the differnce between angular velocity of robot and two consecutive moments of time
        self.kalman_odom_ = Odometry()  # This will store the filtered odometry message

        # Estimate the variances for the motion and measurement models
        self.motion_variance_ = 4.0  # Variance for the motion model

        self.measurement_variance_ = 0.5  # Variance for the measurement model


    def measurementUpdate(self):

        # updated mean
        self.mean_ = (self.measurement_variance_ * self.mean_ + self.variance_ * self.imu_angular_z_) / (self.variance_ + self.measurement_variance_)

        #updated variance
        self.variance_ = (self.variance_ * self.measurement_variance_) / (self.variance_ + self.measurement_variance_)

    def statePrediction(self):

        # Predict the new mean based on the motion model
        self.mean_ += self.motion_

        # Update the variance based on the motion model
        self.variance_ += self.motion_variance_



    def imuCallback(self, imu):
        # Update the IMU angular velocity
        self.imu_angular_z_ = imu.angular_velocity.z


    def odomCallback(self, odom):
        self.kalman_odom_ = odom  # Store the incoming odometry message

        # First estimate of angular velocity from encoders
        if self.is_first_odom_:
            self.mean_ = odom.twist.twist.angular.z
            self.last_angular_z_ = odom.twist.twist.angular.z

            self.is_first_odom_ = False
            return  # Skip the rest of the processing for the first message

        # Calculate the robot motion
        self.motion_ = odom.twist.twist.angular.z - self.last_angular_z_
         

        self.statePrediction()

        self.measurementUpdate( )

        self.kalman_odom_.twist.twist.angular.z = self.mean_
        self.odom_pub.publish(self.kalman_odom_)



def main(args=None):
    rclpy.init(args=args)
    kalman_filter_node = KalmanFilterNode()
    rclpy.spin(kalman_filter_node)
    kalman_filter_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()