#!/usr/bin/env python3

#dependencies 
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time
import math



class ArduinoJoystickPublisher(Node): 
    def __init__(self):
        super().__init__('arduino_joystick_publisher')
        self.get_logger().info('Arduino Joystick Publisher Node initialized')

        # Create publishers, subscribers, services, etc. here
        self.joystick_publisher_ = self.create_publisher(Twist, "cmd_vel", 10)
        self.timer_ = self.create_timer(0.05, self.publish_joystick_values) #publish every 50ms

        self.declare_parameter('serial_port', '/dev/ttyACM0') # Default Arduino port
        self.declare_parameter('baud_rate', 115200)

        self.serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        self.baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value

        self.ser = None
        self.linear_x = 0.0
        self.angular_z = 0.0
        self.button_state = 0

        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            self.get_logger().info(f"Connected to serial port {self.serial_port} at {self.baud_rate} baud")
        except serial.SerialException as e:
            self.get_logger().error(f"Could not open serial port {self.serial_port}: {e}")
            rclpy.shutdown()


    #Add callback functions here
    def publish_joystick_values(self):   # And here is where we actually publish the message
        if self.ser and self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                parts = line.split(',')
                if len(parts) == 3:
                    x_val = int(parts[0])
                    y_val = int(parts[1])
                    btn_state = int(parts[2])
                    self.get_logger().info("x_val received: " + str(x_val))
                    self.get_logger().info("y_val received: " + str(y_val))
                    self.get_logger().info("Button State received: " + str(btn_state))

                    # Map joystick values to robot velocities
                    # Assuming joystick X for linear.x and Y for angular.z
                    # Adjust scaling factors as needed for your robot's speed
                    self.angular_z = (2.00 * x_val / 1006.00)-1
                    if (self.angular_z > 0.0 and self.angular_z < 0.15) or (self.angular_z > -0.15 and self.angular_z < 0):
                        self.angular_z = 0.0
                    self.linear_x = (y_val / 1006.00)-0.5
                    if (self.linear_x > 0.0 and self.linear_x < 0.15) or (self.linear_x > -0.15 and self.linear_x < 0):
                        self.linear_x = 0.0

                    self.get_logger().info("angular_z cmd will be: " + str(self.angular_z))
                    self.get_logger().info("linear_x cmd will be: " + str(self.linear_x))
                    # You can use the button_state for additional commands if needed
                    # e.g., enabling/disabling motors, changing speed modes.
                    # self.get_logger().info(f"Joystick: X={x_val}, Y={y_val}, Button={button_state}")

            except ValueError as e:
                self.get_logger().warn(f"Error parsing serial data: {e} - Line: {line}")
            except Exception as e:
                self.get_logger().error(f"Unexpected error: {e}")

        msg = Twist()
        msg.linear.x = self.linear_x
        msg.angular.z = self.angular_z
        self.joystick_publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoJoystickPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.ser:
            node.ser.close()
            node.get_logger().info("Serial port closed.")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()