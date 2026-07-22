import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-Control/install/bumperbot_py_examples'
