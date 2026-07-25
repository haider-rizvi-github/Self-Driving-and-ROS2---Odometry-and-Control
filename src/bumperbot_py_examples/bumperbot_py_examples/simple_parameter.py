import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter


class SimpleParameterNode(Node):
    def __init__(self):
        super().__init__("simple_parameter_node")

        self.declare_parameter("simple_int", 42)
        self.declare_parameter("simple_param_string", "Haider")

        self.add_on_set_parameters_callback(self.parameter_change_callback)

    def parameter_change_callback(self, params):
        for param in params:
            if param.name == "simple_int":
                if param.type_ != Parameter.Type.INTEGER:
                    return SetParametersResult(
                        successful=False, reason="simple_int must be an integer"
                    )

            elif param.name == "simple_param_string":
                if param.type_ != Parameter.Type.STRING:
                    return SetParametersResult(
                        successful=False, reason="simple_param_string must be a string"
                    )

            else:
                return SetParametersResult(
                    successful=False, reason=f"Unknown parameter: {param.name}"
                )

        # Log only after all parameters have passed validation
        for param in params:
            self.get_logger().info(
                f"Parameter '{param.name}' changed to '{param.value}'"
            )

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = SimpleParameterNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
