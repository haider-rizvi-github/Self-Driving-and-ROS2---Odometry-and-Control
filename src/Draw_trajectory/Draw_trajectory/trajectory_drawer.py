import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped

class Trajectory_Drawer(Node):
    def __init__(self):
        super().__init__("trajectory_drawer")

        self.declare_parameter(
            "odom_topic",
            "bumperbot_controller/odom",
        )

        self.odom_topic=(
            self.get_parameter("odom_topic").get_parameter_value().string_value
        )

        self.trajectory = Path()
        self.trajectory.header.frame_id = "odom"

        self.trajectory_pub = self.create_publisher(
            Path,
            "bumperbot_controller/trajectory",
            10
        ) 

        self.odom_sub = self.create_subscription(
            Odometry,           # message type
            self.odom_topic,         # topic to listen
            self.odom_callback, #Function called for every message
            10                  # Queue Depth   
        )

        self.get_logger().info("Trajectory Drawer started. Listening to %s" % (self.odom_topic))

    def odom_callback(self, msg):

        current_pose = PoseStamped()

        current_pose.header = msg.header
        current_pose.pose = msg.pose.pose

        self.trajectory.header = msg.header

        self.trajectory.poses.append(current_pose)

        self.trajectory_pub.publish(self.trajectory)

def main(args=None):

    rclpy.init(args=args)
    node= Trajectory_Drawer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()