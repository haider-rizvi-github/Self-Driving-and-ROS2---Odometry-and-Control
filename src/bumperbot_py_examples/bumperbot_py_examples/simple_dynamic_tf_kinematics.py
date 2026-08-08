"""
This is a custom made node that will publish the dynamic and static tf transformations of the BumperBot robot.
The dynamic and static transforms are published to the /tf topic and can be visualized in RViz.
'from tf2_ros import TransformBroadcaster' is used to publish dynamic transforms between two frames
"""

import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class SimpleDynamicTfKinematics(Node):
    def __init__(self):
        super().__init__("simple_dynamic_tf_kinematics")
        self.get_logger().info("SimpleDynamicTfKinematics node has been started.")

        self.static_tf_broadcaster = StaticTransformBroadcaster(self)
        self.dynamic_tf_broadcaster = TransformBroadcaster(self)

        self.static_transform_stamped = TransformStamped()
        self.dynamic_transform_stamped = TransformStamped()

        self.x_increment_ = 0.01  # increment in x direction for the dynamic transform
        self.last_x_ = 0.0  # last x position of the dynamic transform

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

        self.dynamic_transform_stamped.header.stamp = self.get_clock().now().to_msg()
        self.dynamic_transform_stamped.header.frame_id = "odom"
        self.dynamic_transform_stamped.child_frame_id = "bumperbot_base"

        # publishing the static transform
        self.static_tf_broadcaster.sendTransform(self.static_transform_stamped)

        self.get_logger().info(
            "Static transform between %s and %s has been published."
            % (
                self.static_transform_stamped.header.frame_id,
                self.static_transform_stamped.child_frame_id,
            )
        )

        self.timer = self.create_timer(0.1, self.timerCallback)

    def timerCallback(self):
        self.dynamic_transform_stamped.header.stamp = self.get_clock().now().to_msg()
        self.dynamic_transform_stamped.header.frame_id = "odom"
        self.dynamic_transform_stamped.child_frame_id = "bumperbot_base"

        # defining the translation between the dynamic transform
        self.dynamic_transform_stamped.transform.translation.x = (
            self.last_x_ + self.x_increment_
        )
        self.dynamic_transform_stamped.transform.translation.y = 0.0
        self.dynamic_transform_stamped.transform.translation.z = 0.0

        # defining the rotation in quaternion format
        self.dynamic_transform_stamped.transform.rotation.x = 0.0
        self.dynamic_transform_stamped.transform.rotation.y = 0.0
        self.dynamic_transform_stamped.transform.rotation.z = 0.0
        self.dynamic_transform_stamped.transform.rotation.w = 1.0

        self.dynamic_tf_broadcaster.sendTransform(self.dynamic_transform_stamped)

        # updating the last_x_ value for the next iteration
        self.last_x_ = self.dynamic_transform_stamped.transform.translation.x


def main(args=None):
    rclpy.init(args=args)
    node = SimpleDynamicTfKinematics()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
