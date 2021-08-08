#!/usr/bin/env python
import numpy as np
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt
import cv2
import time,csv
from csv import writer
import easygui
from easygui import *
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog

def get_value(msg):
	text = msg
	title = "Enter value"
	d_text = ""
	output = enterbox(text, title, d_text)
	return output

def append_xy(file_name, xy):
    with open(file_name, 'a+') as f:
        csv_writer = writer(f)
        csv_writer.writerow(xy)

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),1,(0,0,255),-1)
        mouseX,mouseY = int(x),int(y)

root = Tk()
file_name = tkFileDialog.askopenfilename(initialdir = "/home/n/catkin_ws/",title = "Select IMAGE",filetypes = (("files",("*.png","*.jpg","*.pgm")),("all files","*.*")))
root.destroy()

img = cv2.imread(file_name,0)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

xy = []
while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
	print "Creating data..."
	time.sleep(2)
        break
    elif k == ord('a'):
	xy.append((mouseX,mouseY))
root = Tk()
csv_location = tkFileDialog.askdirectory(initialdir="/home/n/catkin_ws/",title='Where to save data')
root.destroy()

if csv_location != '':
	data = csv_location+"/data.csv"
	append_xy(data,xy) 
	print ("Data successfully saved in: "+data)
	time.sleep(2)




