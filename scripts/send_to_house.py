#!/usr/bin/python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point 
from sound_play.libsoundplay import SoundClient
from time import sleep

# first must run the node: - rosrun sound_play soundplay_node.py
#                          - roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch 
#                          - roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=/
#                          - run python file


class map_navigation():
	
	def choose(self):
		sleep(5)
		choice='q'

		print("|---------------------------|")
		print("|	'0': A             |") 
		print("|	'1': B             |")
		print("|	'2': C             |")
		print("|	'3': D             |")
		print("|	'4': E             |")
		print("|	'5': F             |")
		print("|	'6': G             |")
		print("|	'q': Quit          |")
		print("|---------------------------|")

		path_to_sounds = "/home/y/catkin_ws/sounds/"
		sc = SoundClient()
		sc.playWave(path_to_sounds+"options.wav")


		choice = input()
		return choice

	def __init__(self): 

		sc = SoundClient()
		path_to_sounds = "/home/y/catkin_ws/sounds/"

		# declare the coordinates of interest 
		self.xA , self.yA =  0.36 , 3.463
		self.xB , self.yB =  3.599 , 0.122
		self.xC , self.yC =  10.52 , -0.001
		self.xD , self.yD =  11.299 , 3.216
		self.xE , self.yE =  9.88 , 5.96
		self.xF , self.yF =  0.3145 , 5.877
		self.xG , self.yG =  0.25 , 7.76

		self.goalReached = False
		# initiliaze
        	rospy.init_node('map_navigation', anonymous=False)
		choice = self.choose()
		
		if (choice == 0):

			self.goalReached = self.moveToGoal(self.xA, self.yA)		
		elif (choice == 1):

			self.goalReached = self.moveToGoal(self.xB, self.yB)
		elif (choice == 2):

			self.goalReached = self.moveToGoal(self.xC, self.yC)
		elif (choice == 3):

			self.goalReached = self.moveToGoal(self.xD, self.yD)
		elif (choice == 4):

			self.goalReached = self.moveToGoal(self.xE, self.yE)
		elif (choice == 5):

			self.goalReached = self.moveToGoal(self.xF, self.yF)
		elif (choice == 6):

			self.goalReached = self.moveToGoal(self.xG, self.yG)

		if (choice!='q'):

			if (self.goalReached ) and (choice == 0):
				sc.playWave(path_to_sounds+"pointA.wav")
				#rospy.loginfo("ROBOT already in the point A")

			elif (self.goalReached ) and (choice == 1):
				sc.playWave(path_to_sounds+"pointB.wav")
				#rospy.loginfo("ROBOT already in the point B")

			elif (self.goalReached ) and (choice == 2):
				sc.playWave(path_to_sounds+"pointC.wav")
				#rospy.loginfo("ROBOT already in the point C")

			elif (self.goalReached ) and (choice == 3):
				sc.playWave(path_to_sounds+"pointD.wav")
				#rospy.loginfo("ROBOT already in the point D")

			elif (self.goalReached ) and (choice == 4):
				sc.playWave(path_to_sounds+"pointE.wav")
				#rospy.loginfo("ROBOT already in the point E")

			elif (self.goalReached ) and (choice == 5):
				sc.playWave(path_to_sounds+"pointF.wav")
				#rospy.loginfo("ROBOT already in the point F")

			elif (self.goalReached ) and (choice == 6):
				sc.playWave(path_to_sounds+"pointG.wav")
				#rospy.loginfo("ROBOT already in the point G")

			else:
				rospy.loginfo("Hard Luck!")


		
		while choice != 'q':
			choice = self.choose()
			if (choice == 0):

				self.goalReached = self.moveToGoal(self.xA, self.yA)
			elif (choice == 1):

				self.goalReached = self.moveToGoal(self.xB, self.yB)
			elif (choice == 2):

				self.goalReached = self.moveToGoal(self.xC, self.yC)
			elif (choice == 3):

				self.goalReached = self.moveToGoal(self.xD, self.yD)
			elif (choice == 4):

				self.goalReached = self.moveToGoal(self.xE, self.yE)
			elif (choice == 5):

				self.goalReached = self.moveToGoal(self.xF, self.yF)
			elif (choice == 6):

				self.goalReached = self.moveToGoal(self.xG, self.yG)

			if (choice!='q'):

				if   (self.goalReached) and (choice == 0):
					sleep(2)
					sc.playWave(path_to_sounds+"pointA.wav")
					#rospy.loginfo("ROBOT reached the point A")

				elif (self.goalReached) and (choice == 1):
					sc.playWave(path_to_sounds+"pointB.wav")
					#rospy.loginfo("ROBOT already in the point B")

				elif (self.goalReached) and (choice == 2):
					sc.playWave(path_to_sounds+"pointC.wav")
					#rospy.loginfo("ROBOT already in the point C")

				elif (self.goalReached) and (choice == 3):
					sc.playWave(path_to_sounds+"pointD.wav")
					#rospy.loginfo("ROBOT already in the point D")

				elif (self.goalReached) and (choice == 4):
					sc.playWave(path_to_sounds+"pointE.wav")
					#rospy.loginfo("ROBOT already in the point E")

				elif (self.goalReached) and (choice == 5):
					sc.playWave(path_to_sounds+"pointF.wav")
					#rospy.loginfo("ROBOT already in the point F")

				elif (self.goalReached) and (choice == 6):
					sc.playWave(path_to_sounds+"pointG.wav")
					#vrospy.loginfo("ROBOT already in the point G")

				else:
					rospy.loginfo("Hard Luck!")



	def shutdown(self):
        # stop turtlebot
        	rospy.loginfo("Quit program")
        	rospy.sleep()

	def moveToGoal(self,xGoal,yGoal):

		path_to_sounds = "/home/y/catkin_ws/sounds/"
		sc = SoundClient()
		

		#define a client for to send goal requests to the move_base server through a SimpleActionClient
		ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

		#wait for the action server to come up
		while(not ac.wait_for_server(rospy.Duration.from_sec(7.0))):
			rospy.loginfo("Waiting for the move_base action server to come up")
		
		goal = MoveBaseGoal()

		#set up the frame parameters
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()

		# moving towards the goal*/

		goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
		goal.target_pose.pose.orientation.x = 0.0
		goal.target_pose.pose.orientation.y = 0.0
		goal.target_pose.pose.orientation.z = 0.0
		goal.target_pose.pose.orientation.w = 1.0

		rospy.loginfo("Sending the ROBOT to goal ...")
		ac.send_goal(goal)

		ac.wait_for_result(rospy.Duration(70))

		if(ac.get_state() ==  GoalStatus.SUCCEEDED):

			rospy.loginfo("ROBOT have reached the destination")
			return True
	
		else:
			rospy.loginfo("ROBOT failed to reach the destination")
			return False

if __name__ == '__main__':
    try:
	
	rospy.loginfo("You have reached the destination")
        map_navigation()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("map_navigation node terminated.")
