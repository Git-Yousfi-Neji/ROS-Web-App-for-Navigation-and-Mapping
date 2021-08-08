# -*- coding: utf-8 -*-
"""
Created on Tue Oct 7 11:41:42 2018
@author: Caihao.Cui
"""
from __future__ import print_function

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time

img = cv2.imread('/home/y/catkin_ws/qrimgs/test7.jpg')

def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
    return decodedObjects

for decodedObject in pyzbar.decode(img):
	print (decodedObject[0])

# get the webcam:  
cap = cv2.VideoCapture(0)
adr = 'http://192.168.1.5:8080/video'
cap.open(adr)
cap.set(3,640)
cap.set(4,480)
#1024.0 x 768.0
#1280.0 x 1024.0
time.sleep(1)

font = cv2.FONT_HERSHEY_SIMPLEX

i = 0
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points;
         
        # Number of points in the convex hull
        n = len(hull)     
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)

        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data,'\n')

        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
               
    # Display the resulting frame
    cv2.imshow('frame',frame)


    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
		break
    elif key & 0xFF == ord(' '): # wait for 'space' key to save 
		cv2.imwrite('Capture'+str(i)+'.png', frame)  
		i += 1
		print ("capture saved !")


# When everything done, release the capture
cap.release() 
cv2.destroyAllWindows()

