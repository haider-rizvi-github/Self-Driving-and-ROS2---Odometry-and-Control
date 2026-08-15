#!/usr/bin/env python3

'''
    imu_republisher.py is needed to configure for the robot localization package to work properly. The robot localization package requires an IMU message to be published on the /imu topic. However, the BumperBot's IMU data is published on the /imu/data topic. This script subscribes to the /imu/data topic, repackages the data into a new IMU message, and republishes it on the /imu topic. This allows the robot localization package to receive the necessary IMU data for its calculations.
'''

import rclpy
from rclpy.node import Node
import time
from sensor_msgs.msg import Imu

imu_pub = None  # Global publisher variable

def imuCallback(imu):
    global imu_pub  # Use the global publisher variable
    imu.header.frame_id = "base_footprint_ekf" 
    imu_pub.publish(imu)  # Republish the IMU message on the /imu



def main():
    global imu_pub  # Declare the global publisher variable
    rclpy.init()
    node = Node("imu_republisher_node")
    time.sleep(1)  # Wait for a second to ensure the node is fully initialized

    imu_pub = node.create_publisher(Imu, "imu_ekf", 10)
    imu_sub = node.create_subscription(Imu, "imu", imuCallback, 10)

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()