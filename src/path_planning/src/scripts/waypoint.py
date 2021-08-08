#!/usr/bin/env python

import rospy
import tf
import numpy as np
import matplotlib.pyplot as plt
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest
from math import pi, sqrt, atan2
import cv2
import time,csv
from csv import writer
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog

def play_sound(sound):
	import roslib; roslib.load_manifest('sound_play')
	import rospy
	from sound_play.libsoundplay import SoundClient
	path_to_sounds = "/home/y/catkin_ws/sounds/"
	#rospy.init_node('play_sound_file')
	sound_client = SoundClient()
	rospy.sleep(1)
	sound_client.playWave(path_to_sounds+sound)

def waypts(ptsnbr=3):
	ls = np.linspace
	WAYPOINTS=[]
	file_name = '/home/y/catkin_ws/data.csv'
	if file_name==():
		return

	def read_xy(file_name):
		with open(file_name, "r") as infile:
		    read = csv.reader(infile)
		    for row in read :
			pass
		return row

	pts = [map(float, p.replace('(','').replace(')','').split(',')) for p in read_xy(file_name)]
	for k in range(len(pts)-1):
		WAYPOINTS += [[round(i,3),round(j,3)] for i,j in zip(ls(pts[k][0],pts[k+1][0],ptsnbr) , ls(pts[k][1],pts[k+1][1],ptsnbr))]
	return WAYPOINTS
root = Tk()
img=tkFileDialog.askopenfilename(initialdir="~/catkin_ws/maps/",title="Select the IMAGE",filetypes=(("files",("*.pgm")),("all files","*.*")))
root.destroy()
im = cv2.imread(img)
size = lambda img: tuple(img.shape[1::-1])
height = size(im)[1]


# height = 220 # image height , transformation between the png image and gazebo world
resolution = 0.05 # tranformation between the png image and gazebo world
WAYPOINTS = [[pt[0],height-pt[1]] for pt in waypts()]
WAYPOINTS = [[round(resolution * pt[0],3),round(resolution * pt[1],3)] for pt in WAYPOINTS]

class PID:
    
    # Discrete PID control
    def __init__(self, P=0.0, I=0.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=10, Integrator_min=-10):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.Derivator = Derivator
        self.Integrator = Integrator
        self.Integrator_max = Integrator_max
        self.Integrator_min = Integrator_min
        self.set_point = 0.0
        self.error = 0.0

    def update(self, current_value):
        self.error = self.set_point - current_value
        if self.error > pi:  # specific design for circular situation
            self.error = self.error - 2*pi
        elif self.error < -pi:
            self.error = self.error + 2*pi
        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error
        self.Integrator = self.Integrator + self.error
        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min
        self.I_value = self.Integrator * self.Ki
        PID = self.P_value + self.I_value + self.D_value
        return PID

    def setPoint(self, set_point):
        self.set_point = set_point
        self.Derivator = 0
        self.Integrator = 0

    def setPID(self, set_P=0.0, set_I=0.0, set_D=0.0):
        self.Kp = set_P
        self.Ki = set_I
        self.Kd = set_D

class turtlebot_move():
    def __init__(self):
        rospy.init_node('turtlebot_move', anonymous=False)
        rospy.loginfo("Press CTRL + C to terminate!")
        rospy.on_shutdown(self.stop)

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.pid_theta = PID(0,0,0)  # initialization

        self.odom_sub = rospy.Subscriber("odom", Odometry, self.odom_callback)
        self.vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.vel = Twist()
        self.rate = rospy.Rate(10)
        self.counter = 0
        self.trajectory = list()

        # track a sequence of waypoints
        for point in WAYPOINTS:
            self.move_to_point(point[0], point[1])
            rospy.sleep(1)
        self.stop()
	#path_to_sounds = "~/catkin_ws/sounds/"
	#sc = SoundClient()
	#sc.playWave(path_to_sounds+"robot_reached_the_end_of_the_path.mp3")
        
	play_sound("robot_reached_the_end_of_the_path.mp3")

	rospy.logwarn("Action is done !")

        # plot trajectory
        data = np.array(self.trajectory)
        np.savetxt('trajectory.csv', data, fmt='%f', delimiter=',')
        plt.plot(data[:,0],data[:,1])
        plt.show()


    def move_to_point(self, x, y):
        # Compute orientation for angular vel and direction vector for linear vel
        diff_x = x - self.x
        diff_y = y - self.y
        direction_vector = np.array([diff_x, diff_y])
        direction_vector = direction_vector/sqrt(diff_x*diff_x + diff_y*diff_y)  # normalization
        theta = atan2(diff_y, diff_x)

        # We should adopt different parameters for different kinds of movement
        self.pid_theta.setPID(1, 0, 0)     # P control while steering
        self.pid_theta.setPoint(theta)
        rospy.logwarn("|| PID: set new theta angle = " + str(theta) + " ||")

        # Adjust orientation first
        while not rospy.is_shutdown():
            angular = self.pid_theta.update(self.theta)
            if abs(angular) > 0.2:
                angular = angular/abs(angular)*0.2
            if abs(angular) < 0.01:
                break
            self.vel.linear.x = 0
            self.vel.angular.z = angular
            self.vel_pub.publish(self.vel)
            self.rate.sleep()

        # Have a rest
        self.stop()
        self.pid_theta.setPoint(theta)
        #self.pid_theta.setPID(1, 0, 0)   # PI control while moving
        self.pid_theta.setPID(1, 0.02, 0.2)  # PID control while moving

        # Move to the target point
        while not rospy.is_shutdown():
            diff_x = x - self.x
            diff_y = y - self.y
            vector = np.array([diff_x, diff_y])
            linear = np.dot(vector, direction_vector) # projection
            if abs(linear) > 0.2:
                linear = linear/abs(linear)*0.2

            angular = self.pid_theta.update(self.theta)
            if abs(angular) > 0.2:
                angular = angular/abs(angular)*0.2

            if abs(linear) < 0.01 and abs(angular) < 0.01:
                break
            self.vel.linear.x = linear
            self.vel.angular.z = angular
            self.vel_pub.publish(self.vel)
            self.rate.sleep()

        self.stop()


    def stop(self):
        self.vel.linear.x = 0
        self.vel.angular.z = 0
        self.vel_pub.publish(self.vel)
        rospy.sleep(1)


    def odom_callback(self, msg):
        # Get (x, y, theta) specification from odometry topic
        quarternion = [msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,\
                    msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
        (roll, pitch, yaw) = tf.transformations.euler_from_quaternion(quarternion)
        self.theta = yaw
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        # Make messages saved and prompted in 5Hz rather than 100Hz
        self.counter += 1
        if self.counter == 20:
            self.counter = 0
            self.trajectory.append([self.x,self.y])
            rospy.loginfo("odom: x=" + str(self.x) + ";  y=" + str(self.y) + ";  theta=" + str(self.theta))





if __name__ == '__main__':
    try:
        turtlebot_move()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROBOT reached the end of the path !")
