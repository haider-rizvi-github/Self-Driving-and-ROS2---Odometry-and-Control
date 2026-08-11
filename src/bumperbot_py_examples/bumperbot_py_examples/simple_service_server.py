import rclpy
from rclpy.node import Node
from bumperbot_msgs.srv import AddTwoInts


class SimpleServiceServer(Node):
    def __init__(self):
        super().__init__("simple_service_server")

        # create a new package and store msgs for the service
        self.service_ = self.create_service(
            AddTwoInts, "add_two_ints", self.serviceCallback
        )

        self.get_logger().info("Service server is ready to add two integers.")

    def serviceCallback(self, request, response):
        self.get_logger().info("Incoming request: a=%d, b=%d" % (request.a, request.b))
        response.sum = request.a + request.b
        self.get_logger().info(
            "The Response is: a:%d + b:%d = sum:%d"
            % (request.a, request.b, response.sum)
        )
        return response


def main():
    rclpy.init()
    simple_service_server = SimpleServiceServer()
    rclpy.spin(simple_service_server)
    simple_service_server.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
