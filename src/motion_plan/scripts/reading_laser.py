#!/usr/bin/env python

import rospy
import math
import sys
import tf
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion

# initialize node, publisher and msg type
rospy.init_node("move_robot")
pub = rospy.Publisher("cmd_vel", Twist, queue_size=5)
velocity_msg = Twist()

# we publish the velocity at 50 Hz (50 times per second)
rate = rospy.Rate(50)

# initialize transformation frames
tf_listener = tf.TransformListener()
odom_frame = 'odom'
base_frame = 'base_footprint'

try:
    tf_listener.waitForTransform(odom_frame, 'base_footprint', rospy.Time(), rospy.Duration(1.0))
    base_frame = 'base_footprint'
except (tf.Exception, tf.ConnectivityException, tf.LookupException):
    try:
        tf_listener.waitForTransform(odom_frame, 'base_link', rospy.Time(), rospy.Duration(1.0))
        base_frame = 'base_link'
    except (tf.Exception, tf.ConnectivityException, tf.LookupException):
        rospy.loginfo("Cannot find transform between odom and base_link or base_footprint")
        rospy.signal_shutdown("tf Exception")


def compute_distance(x1, y1, x2, y2):
    """
        function to compute distance between points
        Inputs:
            x1: x-coordinate of point1
            y1: y-coordinate of point1
            x2: x-coordinate of point2
            y2: y-coordinate of point2
        Outputs:
            dist: distance between 2 points
    """
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


def go_straight(linear_velocity):
    """ function to give robot a linear velocity
    Input:
        linear_velocity: desired linear velocity of the robot
    """
    global velocity_msg
    # set linear and angular velocity
    velocity_msg.linear.x = linear_velocity
    velocity_msg.angular.z = 0
    rospy.loginfo("TurtleBot is moving straight")
    # publish velocity message
    pub.publish(velocity_msg)
    rate.sleep()

def rotate(relative_angle_degree, angular_velocity):
    """ function to rotate a robot by a given degree
    Input:
        relative_angle_degree : angle by which to rotate the robot
        angular_velocity : desired angular velocity of the robot
    """

    global velocity_msg
    # set velocity message
    velocity_msg.linear.x = 0
    velocity_msg.angular.z = angular_velocity
    t0 = rospy.Time.now().to_sec()
    # loop until the desired angle is reached
    while True:
        # publish velocity message
        rospy.loginfo("TurtleBot is rotating")
        pub.publish(velocity_msg)
        rate.sleep()
        t1 = rospy.Time.now().to_sec()
        rospy.loginfo("t0: {t}".format(t=t0))
        rospy.loginfo("t1: {t}".format(t=t1))
        # angle by which the robot as rotated
        current_angle_degree = (t1 - t0) * angular_velocity
        rospy.loginfo("current angle: {a}".format(a=current_angle_degree))
        rospy.loginfo("angle to reach: {a}".format(a=relative_angle_degree))
        # check if desired angle has been reached
        if abs(current_angle_degree) >= math.radians(abs(relative_angle_degree)):
            rospy.loginfo("reached")
            break
    # finally, stop the robot when the distance is moved
    velocity_msg.angular.z = 0
    pub.publish(velocity_msg)


def get_odom_data():
    """ function to get odometry data 
    """
    try:
        (trans, rot) = tf_listener.lookupTransform(odom_frame, base_frame, rospy.Time(0))
        rotation = euler_from_quaternion(rot)
    except (tf.Exception, tf.ConnectivityException, tf.LookupException):
        rospy.loginfo("TF Exception")
        return

    return Point(*trans), rotation[2]


# initialize global variables
front = 0
left_15 = 0
right_15 = 0
left_90 = 0
right_90 = 0
left_110 = 0
back = 0
left_44 = 0
left_45 = 0
left_46 = 0
right_89 = 0
right_91 = 0


def sensor_callback(msg):
    """callback function for the scan subscriber
    """
    # global variables
    global front
    global left_15
    global right_15
    global left_90
    global right_90
    global back
    global left_110
    global left_44
    global left_45
    global left_46
    global right_89
    global right_91

    # read laser scan data
    front = msg.ranges[0]
    left_15 = msg.ranges[25]
    right_15 = msg.ranges[335]
    left_90 = msg.ranges[90]
    right_90 = msg.ranges[270]
    back = msg.ranges[180]
    left_110 = msg.ranges[110]
    left_44 = msg.ranges[44]
    left_45 = msg.ranges[45]
    left_46 = msg.ranges[46]
    right_89 = msg.ranges[271]
    right_91 = msg.ranges[269]


# initialize subscriber
rospy.Subscriber("scan", LaserScan, sensor_callback)


def find_wall():
    """function to find the closest wall
    Returns:
        nearest_wall: location of nearest wall - front, left, right, back
        distance: distance to the nearest wall
    """

    # initialize global variables
    global front
    global left_15
    global right_15
    global left_90
    global right_90
    global back

    # dictionary of object distance on all four sides of the robot
    obstacle_dict = {'front': front,
                     'left': left_90,
                     'right': right_90,
                     'back': back}

    # find nearest wall
    nearest_wall = min(obstacle_dict, key=obstacle_dict.get)
    rospy.loginfo('Closest wall found on {} of the robot at a distance of {}'.format(nearest_wall,obstacle_dict[nearest_wall]))
    # distance of nearest wall
    distance = obstacle_dict[nearest_wall]

    # give preference to left wall
    if abs(distance - left_90) <= 5:
        nearest_wall = 'left'
        distance = obstacle_dict[nearest_wall]

    # 2nd preference to the wall behind the robot
    elif abs(distance - back) <= 5:
        nearest_wall = 'back'
        distance = obstacle_dict[nearest_wall]
    return nearest_wall, distance


def go_to_wall(nearest_wall):
    """ drive robot to the nearest wall
    Args:
        nearest_wall: location of the nearest wall (front, left, right, back)
    """

    # initialize global variables
    global front
    global left_15
    global right_15
    global left_90
    global right_90
    global back

    # distance of the robot to the wall
    thresh = 0.25

    # if nearest wall is in the front of robot
    if nearest_wall == 'front':
        while front > thresh:
            go_straight(0.2)
        rotate(-90, -0.1)
    # if nearest wall is in the left of robot
    elif nearest_wall == 'left':
        rotate(90, 0.1)
        while front > thresh:
            go_straight(0.2)
        rotate(-90, -0.1)
    # if nearest wall is in the right of robot
    elif nearest_wall == 'right':
        rotate(-90, -0.1)
        while front > thresh:
            go_straight(0.2)
        rotate(-90, -0.1)
    # if nearest wall is in the back of robot
    elif nearest_wall == 'back':
        rotate(180, 0.1)
        while front > thresh:
            go_straight(0.2)
        rotate(-90, -0.1)


def check_left_turn():
    """ check whether a left turn is available
    Returns:
        True of False - whether left turn is available or not
    """

    # distance of object at front left
    left2 = (left_44 + left_45 + left_46)/3
    if front > 1.0 and left2 > 1.0:
        return True
    else:
        return False


def check_right_turn():
    """ check whether a right turn is available
    Returns:
        True of False - whether right turn is available or not
    """
    # distance of object at right of the robot
    right2 = (right_89 + right_90 + right_91) / 3
    if right2 > 1.5:
        return True
    else:
        return False

# goal location
goal_x,goal_y = (15.82, 3.8)

wall_found = False
error_prev = 0

# parameters for PD controller
Kp = 2
Kd = 0.4
state = 'find_wall'

# while goal has not been reached
while True:

    # get position and orientation of the robot
    (position, rotation) = get_odom_data()

    # distance to goal
    distance_to_goal = compute_distance(position.x, position.y, goal_x, goal_y)
    # break if goal has been reached
    if distance_to_goal <= 1:
        rospy.loginfo('Goal has been reached')
        # stop the robot
        velocity_msg.linear.x = 0
        velocity_msg.angular.z = 0
        pub.publish(velocity_msg)
        break

    # find wall
    if state == 'find_wall':
        nearest_wall, distance = find_wall()
        # if wall found, go to wall
        if distance > 0:
            state = 'follow_wall'
            go_to_wall(nearest_wall)

    # check if left turn is possible
    elif check_left_turn():
        rospy.loginfo('left turn detected')
        # if turn possible, go straight until turn is reached
        if front > 0.25:
            go_straight(0.1)
        else:
            rotate(-90, -0.2)

        if left_90 > 1.5 and left_110 > 1.5:
            # rotate 90 towards left (anticlockwise)
            rotate(90, 0.2)
            # go straight after rotating
            while left_90 > 1:
                go_straight(0.2)

    # check if robot can go straight
    elif state == 'follow_wall' and front > 0.25:
        # distance of wall at front left of the robot
        left1 = (left_44 + left_45 + left_46)/3
        # ratio of distance at left and front left of the robot
        # secant of the angle
        orientation = left1/left_90
        max_angular = 0.1
        rospy.loginfo('distance at left {}'.format(left_90))
        # 1.414 is square root of 2
        # angle will be 45 when the robot is parallel to the wall
        error = orientation-1.414

        # if robot is parallel to the wall (within some error range)
        if 1.39 <= orientation <= 1.43:
            rospy.loginfo('going straight')
            velocity_msg.linear.x = 0.4
            velocity_msg.angular.z = 0

        # if robot is pointed away from the wall
        elif orientation > 1.43:
            # rotate left
            rospy.loginfo('adjusting by turning left')
            velocity_msg.linear.x = 0
            # angular velocity using PD control
            velocity_msg.angular.z = 1.5*max_angular * ((Kp * error) + Kd * (error - error_prev)/0.05)

        # if robot is pointed towards the wall
        elif orientation < 1.39:
            # rotate right
            rospy.loginfo('adjusting by turning right')
            # angular velocity using PD control
            velocity_msg.linear.x = 0
            velocity_msg.angular.z = 4.5*max_angular * ((Kp * error) + Kd * (error - error_prev)/0.05)
        # publish velocity message
        pub.publish(velocity_msg)
        rate.sleep()
        error_prev = error

    # check if right turn is possible
    elif check_right_turn():
        rotate(-90, -0.2)
    # turn around if path is blocked
    else:
        rotate(180, 0.2)
