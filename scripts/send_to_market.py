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

		print("|---------------------------------|")
		print("|	'0': CAFE                |") 
		print("|	'1': OFFICE-1            |")
		print("|	'2': OFFICE-2            |")
		print("|	'3': OFFICE-3            |")
		print("|	'q': Quit                |")
		print("|---------------------------------|")

		path_to_sounds = "/home/y/catkin_ws/sounds/"
		sc = SoundClient()
		sc.playWave(path_to_sounds+"options.wav")

		choice = input()
		return choice

	def __init__(self): 

		sc = SoundClient()
		path_to_sounds = "/home/y/catkin_ws/sounds/"

		# declare the coordinates of interest 
		self.xCafe    , self.yCafe    = 4.489 , 6.6525
		self.xOffice1 , self.yOffice1 = 2.466 , 6.162
		self.xOffice2 , self.yOffice2 = 2.57 , 3.02
		self.xOffice3 , self.yOffice3 = 7.7391 , 3.0047

		self.goalReached = False
		# initiliaze
        	rospy.init_node('map_navigation', anonymous=False)
		choice = self.choose()
		
		if (choice == 0):

			self.goalReached = self.moveToGoal(self.xCafe, self.yCafe)
		elif (choice == 1):

			self.goalReached = self.moveToGoal(self.xOffice1, self.yOffice1)
		elif (choice == 2):
			
			self.goalReached = self.moveToGoal(self.xOffice2, self.yOffice2)
		elif (choice == 3):

			self.goalReached = self.moveToGoal(self.xOffice3, self.yOffice3)
		if (choice!='q'):

			if (self.goalReached ) and (choice == 0):
				sc.playWave(path_to_sounds+"cafe.wav")

			elif (self.goalReached ) and (choice == 1):
				sc.playWave(path_to_sounds+"office1.wav")

			elif (self.goalReached ) and (choice == 2):
				sc.playWave(path_to_sounds+"office2.wav")

			elif (self.goalReached ) and (choice == 3):
				sc.playWave(path_to_sounds+"office3.wav")

			else:
				rospy.loginfo("Hard Luck!")
		
		while choice != 'q':
			choice = self.choose()
			if (choice == 0):

				self.goalReached = self.moveToGoal(self.xCafe, self.yCafe)
			elif (choice == 1):

				self.goalReached = self.moveToGoal(self.xOffice1, self.yOffice1)
			elif (choice == 2):
		
				self.goalReached = self.moveToGoal(self.xOffice2, self.yOffice2)
			elif (choice == 3):

				self.goalReached = self.moveToGoal(self.xOffice3, self.yOffice3)
			if (choice!='q'):

				if (self.goalReached ) and (choice == 0):
					sc.playWave(path_to_sounds+"cafe.wav")

				elif (self.goalReached ) and (choice == 1):
					sc.playWave(path_to_sounds+"office1.wav")

				elif (self.goalReached ) and (choice == 2):
					sc.playWave(path_to_sounds+"office2.wav")

				elif (self.goalReached ) and (choice == 3):
					sc.playWave(path_to_sounds+"office3.wav")

				else:
					rospy.loginfo("Hard Luck!")


	def shutdown(self):
        # stop turtlebot
        	rospy.loginfo("Quit program")
        	rospy.sleep()

	def moveToGoal(self,xGoal,yGoal):

		#define a client for to send goal requests to the move_base server through a SimpleActionClient
		ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

		#wait for the action server to come up
		while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
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

		ac.wait_for_result(rospy.Duration(60))

		if(ac.get_state() ==  GoalStatus.SUCCEEDED):
			rospy.loginfo("ROBOT reached the destination")	
			return True
	
		else:
			rospy.loginfo("ROBOT failed to reach the destination")
			return False

if __name__ == '__main__':
    try:
	
	rospy.loginfo("ROBOT reached the destination")
        map_navigation()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("map_navigation node terminated.")
