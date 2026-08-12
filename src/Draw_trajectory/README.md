Draw_trajectory
=================

Overview
--------
This package provides a small ROS 2 Python node that listens to odometry messages and publishes a Path message representing the vehicle's trajectory. It is intended for visualization (for example, in RViz) of the bumperbot's past poses.

Key implementation file
-----------------------
- [trajectory_drawer.py](/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-Control/src/Draw_trajectory/Draw_trajectory/trajectory_drawer.py)

Other package files
-------------------
- [package.xml](/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-Control/src/Draw_trajectory/package.xml)
- [setup.py](/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-RO S2---Odometry-and-Control/src/Draw_trajectory/setup.py)  (used to install the console script entry point)

How the node works
------------------
The node class in [trajectory_drawer.py](/home/syed/Desktop/Self-Driving-and-ROS2---Odometry-and-Control/src/Draw_trajectory/Draw_trajectory/trajectory_drawer.py) is Trajectory_Drawer and does the following:

1. Initialization
   - Declares a parameter named `odom_topic` with a default value of `bumperbot_controller/odom`.
   - Reads the parameter and stores it in `self.odom_topic`.
   - Creates a Path message (`self.trajectory`) and sets its header frame_id to `odom`.
   - Creates a publisher that publishes `nav_msgs/Path` messages on topic `bumperbot_controller/trajectory`.
   - Creates a subscription to the odometry topic (type `nav_msgs/Odometry`) using `self.odom_topic`.
   - Logs an info message indicating that the node is started and which odometry topic it listens to.

2. odom_callback (called for every incoming Odometry message)
   - Creates a new `geometry_msgs/PoseStamped` message named `current_pose`.
   - Copies the incoming odometry message's `header` and `pose.pose` into `current_pose.header` and `current_pose.pose` respectively.
   - Updates `self.trajectory.header` to match the incoming message's header (so the Path has an up-to-date timestamp/frame).
   - Appends `current_pose` to `self.trajectory.poses`.
   - Publishes `self.trajectory` on the `bumperbot_controller/trajectory` topic.

Important details and behavior
------------------------------
- The node accumulates poses in memory. Each received Odometry message appends another pose to the Path. Over long runs this list will grow indefinitely; if running for long durations consider adding pruning or limiting the number of stored poses.

- The Path.header.frame_id is set to `odom` in initialization. The odom messages' headers are copied to each PoseStamped and to the Path header, so the Path timestamps and frames follow the odometry input.

- The default odometry input topic is `bumperbot_controller/odom`. Override this at runtime by passing a parameter (see usage below).

- The console script entry point `trajectory_drawer` is registered in setup.py, mapping to `Draw_trajectory.trajectory_drawer:main`. That means the node can be started using `ros2 run` once the package is installed or sourced.

Running the node
----------------
If the workspace is built and sourced (colcon build && . install/setup.bash), run the node with:

ros2 run Draw_trajectory trajectory_drawer

To override the odometry topic (for example if odometry is published on `/odom`):

ros2 run Draw_trajectory trajectory_drawer --ros-args -p odom_topic:=/odom

To view the published trajectory in RViz, add a Path display and set the topic to `bumperbot_controller/trajectory` (or the topic chosen by your configuration).

Notes and suggested improvements
-------------------------------
- Consider clearing or limiting the number of stored poses to avoid unbounded memory growth. For example, keep only the last N poses or remove poses older than a configured time window.

- Consider providing a parameter for the output topic name and the frame_id (currently hard-coded to `odom` and `bumperbot_controller/trajectory`).

- If expecting high-frequency Odometry messages and only a downsampled trajectory is useful for visualization, add a downsampling parameter (publish every N-th message).

Contact
-------
Maintainer: syed <serveronthego1@gmail.com>

