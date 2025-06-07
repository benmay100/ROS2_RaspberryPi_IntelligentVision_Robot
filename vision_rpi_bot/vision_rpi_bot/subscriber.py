#!/usr/bin/env python3

# dependencies 
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class PythonSubscriber(Node):
    def __init__(self):
        super().__init__('python_subscriber')
        self.get_logger().info('Python Subscriber Node initialized')

        # Create publishers, subscribers, services, etc. here
        self.subscriber_ = self.create_subscription(Int64, "python_publisher_topic", self.callback_python_publisher_topic, 10)


    #Add callback functions here
    def callback_python_publisher_topic(self, msg):
        self.get_logger().info("Number received: " + str(msg.data))



def main(args=None):
    rclpy.init(args=args)
    node = PythonSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()