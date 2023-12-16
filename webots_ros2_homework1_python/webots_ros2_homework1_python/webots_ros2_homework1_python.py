import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile
from std_msgs.msg import Empty
import numpy as np
from math import sin, cos, pi, atan2
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import time
import sys

class AutoParking(Node):
    def __init__(self):
        super().__init__('AutoParking')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 1)
        self.reset_pub = self.create_publisher(Empty, '/reset', 1)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.r = self.create_rate(10)  # Adjust the rate as needed
        self.msg = LaserScan()
        self.step = 0
        self.twist = Twist()
        self.reset = Empty()
        self.rotation_point = None
        self.theta = 0.0

    def scan_callback(self, msg):
        self.msg = msg

    def odom_callback(self, odom):
        yaw = self.quaternion(odom)
        if self.step == 0:
            scan_done, center_angle, start_angle, end_angle = self.scan_parking_spot()

            if scan_done:
                fining_spot, start_point, center_point, end_point = self.finding_spot_position(center_angle, start_angle, end_angle)
                if fining_spot:
                    self.theta = np.arctan2(start_point[1] - end_point[1], start_point[0] - end_point[0])
                    print("=================================")
                    print("|        |     x     |     y     |")
                    print('| start  | {0:>10.3f}| {1:>10.3f}|'.format(start_point[0], start_point[1]))
                    print('| center | {0:>10.3f}| {1:>10.3f}|'.format(center_point[0], center_point[1]))
                    print('| end    | {0:>10.3f}| {1:>10.3f}|'.format(end_point[0], end_point[1]))
                    print("=================================")
                    print('| theta  | {0:.2f} deg'.format(np.rad2deg(self.theta)))
                    print('| yaw    | {0:.2f} deg'.format(np.rad2deg(yaw)))
                    print("=================================")
                    print("===== Go to parking spot!!! =====")
                    self.step = 1
                else:
                    print("Fail finding parking spot.")

        elif self.step == 1:
            init_yaw = yaw
            yaw = self.theta + yaw
            if self.theta > 0:
                if self.theta - init_yaw > 0.1:
                    self.twist.linear.x = 0.0
                    self.twist.angular.z = 0.2
                else:
                    self.twist.linear.x = 0.0
                    self.twist.angular.z = 0.0
                    self.cmd_pub.publish(self.twist)
                    time.sleep(1)
                    self.reset_pub.publish(self.reset)
                    time.sleep(3)
                    self.rotation_point = self.rotate_origin_only(center_point[0], center_point[1], -(pi / 2 - init_yaw))
                    self.step = 2
            else:
                if self.theta - init_yaw < -0.1:
                    self.twist.linear.x = 0.0
                    self.twist.angular.z = -0.2
                else:
                    self.twist.linear.x = 0.0
                    self.twist.angular.z = 0.0
                    self.cmd_pub.publish(self.twist)
                    time.sleep(1)
                    self.reset_pub.publish(self.reset)
                    time.sleep(3)
                    self.rotation_point = self.rotate_origin_only(center_point[0], center_point[1], -(pi / 2 - init_yaw))
                    self.step = 2

        elif self.step == 2:
            if abs(odom.pose.pose.position.x - (self.rotation_point[1])) > 0.02:
                if odom.pose.pose.position.x > (self.rotation_point[1]):
                    self.twist.linear.x = -0.05
                    self.twist.angular.z = 0.0
                else:
                    self.twist.linear.x = 0.05
                    self.twist.angular.z = 0.0
            else:
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.step = 3

        elif self.step == 3:
            if yaw > -pi / 2:
                self.twist.linear.x = 0.0
                self.twist.angular.z = -0.2
            else:
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.step = 4

        elif self.step == 4:
            ranges = []
            for i in range(150, 210):
                if self.msg.ranges[i] != 0:
                    ranges.append(self.msg.ranges[i])
            if min(ranges) > 0.2:
                self.twist.linear.x = -0.04
                self.twist.angular.z = 0.0
            else:
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                print("Auto_parking Done.")
                self.cmd_pub.publish(self.twist)
                sys.exit()

        self.cmd_pub.publish(self.twist)
        self.scan_spot_filter(center_angle, start_angle, end_angle)

    def scan_parking_spot(self):
        intensity_index = []
        index_count = []
        spot_angle_index = []
        minimum_scan_angle = 30
        maximum_scan_angle = 330
        intensity_threshold = 100
        center_angle = 0
        start_angle = 0
        end_angle = 0

        for i in range(360):
            if minimum_scan_angle <= i < maximum_scan_angle:
                spot_intensity = self.msg.intensities[i] ** 2 * self.msg.ranges[i] / 100000
                if spot_intensity >= intensity_threshold:
                    intensity_index.append(i)
                    index_count.append(i)
                else:
                    intensity_index.append(0)
            else:
                intensity_index.append(0)

        for i in index_count:
            if abs(i - index_count[int(len(index_count) / 2)]) < 20:
                spot_angle_index.append(i)
                if len(spot_angle_index) > 10:
                    center_angle = spot_angle_index[int(len(spot_angle_index) / 2)]
                    start_angle = spot_angle_index[2]
                    end_angle = spot_angle_index[-3]

        return True, center_angle, start_angle, end_angle

    def quaternion(self, odom):
        quaternion = (
            odom.pose.pose.orientation.x,
            odom.pose.pose.orientation.y,
            odom.pose.pose.orientation.z,
            odom.pose.pose.orientation.w)
        euler = euler_from_quaternion(quaternion)
        yaw = euler[2]
        return yaw

    def get_angle_distance(self, angle):
        distance = self.msg.ranges[int(angle)]
        if self.msg.ranges[int(angle)] is not None and distance != 0:
            angle = int(angle)
            distance = distance
        return angle, distance

    def get_point(self, start_angle_distance):
        angle = start_angle_distance[0]
        angle = np.deg2rad(angle - 180)
        distance = start_angle_distance[1]

        if 0 <= angle < pi / 2:
            x = distance * cos(angle) * -1
            y = distance * sin(angle) * -1
        elif pi / 2 <= angle < pi:
            x = distance * cos(angle) * -1
            y = distance * sin(angle) * -1
        elif -pi / 2 <= angle < 0:
            x = distance * cos(angle) * -1
            y = distance * sin(angle) * -1
        else:
            x = distance * cos(angle) * -1
            y = distance * sin(angle) * -1

        return [x, y]

    def finding_spot_position(self, center_angle, start_angle, end_angle):
        print("scan parking spot done!")
        finding_spot = False
        start_angle_distance = self.get_angle_distance(start_angle)
        center_angle_distance = self.get_angle_distance(center_angle)
        end_angle_distance = self.get_angle_distance(end_angle)

        if start_angle_distance[1] != 0 and center_angle_distance[1] != 0 and end_angle_distance[1] != 0:
            print("calibration......")
            start_point = self.get_point(start_angle_distance)
            center_point = self.get_point(center_angle_distance)
            end_point = self.get_point(end_angle_distance)
            finding_spot = True
        else:
            finding_spot = False
            print("wrong scan!!")

        return finding_spot, start_point, center_point, end_point

    def rotate_origin_only(self, x, y, radians):
        xx = x * cos(radians) + y * sin(radians)
        yy = -x * sin(radians) + y * cos(radians)
        return xx, yy

    def scan_spot_filter(self, center_angle, start_angle, end_angle):
        scan_spot_pub = self.create_publisher(LaserScan, "/scan_spot", 1)
        scan_spot = self.msg
        scan_spot_list = list(scan_spot.intensities)
        for i in range(360):
            scan_spot_list[i] = 0
        scan_spot_list[start_angle] = self.msg.ranges[start_angle] + 10000
        scan_spot_list[center_angle] = self.msg.ranges[center_angle] + 10000
        scan_spot_list[end_angle] = self.msg.ranges[end_angle] + 10000
        scan_spot.intensities = tuple(scan_spot_list)
        scan_spot_pub.publish(scan_spot)

def main(args=None):
    rclpy.init(args=args)
    auto_parking = AutoParking()
    rclpy.spin(auto_parking)
    auto_parking.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
