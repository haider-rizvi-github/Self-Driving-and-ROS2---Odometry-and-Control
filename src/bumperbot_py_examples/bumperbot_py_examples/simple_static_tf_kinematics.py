"""
This is a custom made node that will publish the static tf transformations of the BumperBot robot.
The static transforms are published to the /tf_static topic and can be visualized in RViz.
'from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster' is used to publish static transforms between two static frames
"""

import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class SimpleTfKinematics(Node):
    def __init__(self):
        super().__init__("simple_tf_kinematics")
        self.get_logger().info("SimpleTfKinematics node has been started.")

        self.static_tf_broadcaster = StaticTransformBroadcaster(self)

        self.static_transform_stamped = TransformStamped()
        self.static_transform_stamped.header.stamp = self.get_clock().now().to_msg()

        # defining the static transform between two frames
        self.static_transform_stamped.header.frame_id = "bumperbot_base"
        self.static_transform_stamped.child_frame_id = "bumperbot_top"

        # defining the translation and rotation between the static transform
        self.static_transform_stamped.transform.translation.x = 0.0
        self.static_transform_stamped.transform.translation.y = 0.0
        self.static_transform_stamped.transform.translation.z = 0.3  # 30cm

        # defining the rotation in quaternion format
        self.static_transform_stamped.transform.rotation.x = 0.0
        self.static_transform_stamped.transform.rotation.y = 0.0
        self.static_transform_stamped.transform.rotation.z = 0.0
        self.static_transform_stamped.transform.rotation.w = 1.0

        # publishing the static transform
        self.static_tf_broadcaster.sendTransform(self.static_transform_stamped)

        self.get_logger().info(
            "Static transform between %s and %s has been published."
            % (
                self.static_transform_stamped.header.frame_id,
                self.static_transform_stamped.child_frame_id,
            )
        )


def main(args=None):
    rclpy.init(args=args)
    node = SimpleTfKinematics()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
