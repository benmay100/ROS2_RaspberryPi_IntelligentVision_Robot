#!/usr/bin/env python3

#dependencies 
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class PythonPublisher(Node): 
    def __init__(self):
        super().__init__('rpi_python_publisher')
        self.get_logger().info('Python Publisher Node initialized')

        # Create publishers, subscribers, services, etc. here
        self.publisher_ = self.create_publisher(Int64, "python_publisher_topic", 10)
        self.timer_ = self.create_timer(2, self.publish_something)

        self.counter_ = 0


    #Add callback functions here
    def publish_something(self):   # And here is where we actually publish the message
        msg = Int64()
        msg.data = self.counter_
        self.publisher_.publish(msg)
        self.counter_ += 1


def main(args=None):
    rclpy.init(args=args)
    node = PythonPublisher()  # REPEAT CUSTOM CLASS NAME FOR THE NODE 
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

