import numpy as np
import cv2
import math
import os.path
from easygui import *
from time import sleep


from Tkinter import *

import Tkinter, Tkconstants, tkFileDialog

def msg(message):
	title = "Message box"
			# text of the Ok button
	ok_btn_txt = "OK"
			# creating a message box
	output = msgbox(message, title, ok_btn_txt)


def get_value(msg):
	# message to be displayed
	text = msg
	title = "Enter value"
	d_text = ""
	output = enterbox(text, title, d_text)
	return output





#
#  This is a start for the map program
#
prompt = '---> '
#print "What is the name of your floor plan you want to convert to a ROS map:" 
#file_name = raw_input(prompt)
file_name = tkFileDialog.askopenfilename(initialdir = "/home/n/catkin_ws",title = "Select floor plan image",filetypes = (("png files","*.png"),("all files","*.*")))
root = Tk()
msg("Choose the X coordinates HORIZANTALLY ! \n\n Double Click the first point !")
root.destroy()
#print "You will need to choose the x coordinates horizontal with respect to each other"
#print "Double Click the first x point to scale"
#
# Read in the image
#
image = cv2.imread(file_name)
#
# Some variables
#
ix,iy = -1,-1
x1 = [0,0,0,0]
y1 = [0,0,0,0]
font = cv2.FONT_HERSHEY_SIMPLEX
#
# mouse callback function
# This allows me to point and 
# it prompts me from the command line
#
def draw_point(event,x,y,flags,param):
    global ix,iy,x1,y1n,sx,sy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        ix,iy = x,y
        print ix,iy
#
# Draws the point with lines around it so you can see it
#
        image[iy,ix]=(0,0,255)
        cv2.line(image,(ix+2,iy),(ix+10,iy),(0,0,255),1)
        cv2.line(image,(ix-2,iy),(ix-10,iy),(0,0,255),1)
	cv2.line(image,(ix,iy+2),(ix,iy+10),(0,0,255),1)
        cv2.line(image,(ix,iy-2),(ix,iy-10),(0,0,255),1)
#
# This is for the 4 mouse clicks and the x and y lengths
#
        if x1[0] == 0:
           x1[0]=ix
           y1[0]=iy
           msg('Double click the second X point !' )
           #print 'Double click a second x point'   
        elif (x1[0] != 0 and x1[1] == 0):
           x1[1]=ix
           y1[1]=iy
           prompt = '> '
           
           #print "What is the x distance in meters between the 2 points?" 
           #deltax = float(raw_input(prompt))
           deltax = float(get_value("distance between the 2 points?(in meters)" ))
           dx = math.sqrt((x1[1]-x1[0])**2 + (y1[1]-y1[0])**2)*.05
           sx = deltax / dx
	   #print "You will need to choose the y coordinates vertical with respect to each other"
	   msg("Choose the Y coordinates VERTICALLY ! \n\n Double Click the first point !")
           #print 'Double Click a y point'

        elif (x1[1] != 0 and x1[2] == 0):
           x1[2]=ix
           y1[2]=iy
           #print 'Double click a second y point'
           msg('Double click the second Y point !')
        else:
           prompt = '> '
           #print "What is the y distance in meters between the 2 points?" 
           #deltay = float(raw_input(prompt))
           deltay = float(get_value("Distance between the 2 points?(in meters)" ))
           x1[3]=ix
           y1[3]=iy    
           dy = math.sqrt((x1[3]-x1[2])**2 + (y1[3]-y1[2])**2)*.05
           sy = deltay/dy 
           print sx, sy
           res = cv2.resize(image, None, fx=sx, fy=sy, interpolation = cv2.INTER_CUBIC)
           cv2.imwrite("Corrected_map.pgm", res );
           cv2.imshow("Image2", res)
           #for i in range(0,res.shape[1],20):
               #for j in range(0,res.shape[0],20):
                   #res[j][i][0] = 0
                   #res[j][i][1] = 0
                   #res[j][i][2] = 0
           #cv2.imwrite("KEC_BuildingCorrectedDots.pgm",res)
	   # Show the image in a new window
	   #  Open a file
	   prompt = '> '
	   #print "What is the name of the new map?"
	   mapName = get_value("Name of the new map?")
	   #mapName = raw_input(prompt)
	   
	   prompt = '> '
	   #print "Where is the desired location of the map and yaml file?" 
	   #print "NOTE: if this program is not run on the TurtleBot, Please input the file location of where the map should be saved on TurtleBot. The file will be saved at that location on this computer. Please then tranfer the files to TurtleBot." 
	   root = Tkinter.Tk()
	   root.withdraw()
	   mapLocation = tkFileDialog.askdirectory(parent=root,initialdir="/home/n/catkin_ws",title='Select where to save your files')
	   root.destroy()
	   #mapLocation = raw_input(prompt)
	   completeFileNameMap = os.path.join(mapLocation, mapName +".pgm")
	   completeFileNameYaml = os.path.join(mapLocation, mapName +".yaml")
	   yaml = open(completeFileNameYaml, "w")
	   cv2.imwrite(completeFileNameMap, res );
	   #
	   # Write some information into the file
	   #
	   yaml.write("image: " + mapLocation + "/" + mapName + ".pgm\n")
	   yaml.write("resolution: 0.050000\n")
	   yaml.write("origin: [" + str(-0.1) + "," +  str(-0.1) + ", 0.0]\n")
	   yaml.write("negate: 0\noccupied_thresh: 0.65\nfree_thresh: 0.196")
	   yaml.close()
	   exit()

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image',draw_point)
#
#  Waiting for a Esc hit to quit and close everything
#
#msg('Files sucessfully saved !')
#sleep(3)
#cv2.destroyAllWindows()

while(1):
    cv2.imshow('image',image)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
       break
    elif k == ord('a'):
       print 'Done'
cv2.destroyAllWindows()

