#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class OdomBroadcaster(Node):
    def __init__(self):
        super().__init__('odom_broadcaster')

        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)

        # Publish at fixed rate so TF tree stays connected even when idle
        self.timer = self.create_timer(0.05, self.publish_odom)

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.vx = 0.0
        self.vy = 0.0
        self.vth = 0.0

        self.last_time = self.get_clock().now()

    def cmd_vel_callback(self, msg):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        delta_x = (self.vx * math.cos(self.theta) - self.vy * math.sin(self.theta)) * dt
        delta_y = (self.vx * math.sin(self.theta) + self.vy * math.cos(self.theta)) * dt
        delta_th = self.vth * dt

        self.x += delta_x
        self.y += delta_y
        self.theta += delta_th

        self.vx = msg.linear.x
        self.vy = msg.linear.y
        self.vth = msg.angular.z

    def publish_odom(self):
        current_time = self.get_clock().now()

        qz = math.sin(self.theta * 0.5)
        qw = math.cos(self.theta * 0.5)

        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        odom.twist.twist.linear.x = self.vx
        odom.twist.twist.linear.y = self.vy
        odom.twist.twist.angular.z = self.vth

        self.odom_pub.publish(odom)


def main(args=None):
    rclpy.init(args=args)
    node = OdomBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
