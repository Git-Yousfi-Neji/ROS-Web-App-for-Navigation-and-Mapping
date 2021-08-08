from easygui import *
from tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import sqlite3
from sqlite3 import Error
from random import *
import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
from pygame import mixer
import time

# ----------------------------------------------------------------------------
database = r"/home/y/catkin_ws/superstore/superstore.sqlite"
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

conn = create_connection(database)

def SELECT_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM superstore")
    rows = cur.fetchall()
    for row in rows:
        print row

def SELECT_X_by_Product_Id(Product_Id, X, conn=create_connection(database)):
    cur = conn.cursor()
    cur.execute("SELECT "+ X +" FROM superstore WHERE Product_Id=?", (Product_Id,))
    Xs = cur.fetchall()
    for x in Xs:
        return x[0]

def Quantity(Product_Id,conn = create_connection(database)):
    cur = conn.cursor()
    cur.execute("SELECT Quantity FROM superstore WHERE Product_Id=?", (Product_Id,))
    Quantities = cur.fetchall()
    for Quantity in Quantities:
        return Quantity[0]

def msg_box(message):
    title = ""
    ok_btn_txt = "OK"
    output = msgbox(message, title, ok_btn_txt)

def play_sound(sound):
    mixer.init()
    mixer.music.load('/home/y/catkin_ws/sounds/'+str(sound))
    mixer.music.play()
    time.sleep(1)
    mixer.music.stop()

def summary(Product_Id, conn = create_connection(database)):

    print '[--------------------------------- SUMMARY ------------------------------------]'
    print '|    Product ID: '+str(Product_Id)
    print '|    Row ID: '+str(SELECT_X_by_Product_Id(Product_Id, 'Row_Id'))
    print '|    Product Name: '+str(SELECT_X_by_Product_Id(Product_Id, 'Product_Name'))
    print '|    Quantity: '+str(Quantity(Product_Id))
    print '|    Shelve out of stock !'
    print '[------------------------------------------------------------------------------]'


#------------------------------------------------------------------------------------
cap = cv2.VideoCapture(0)
adr = 'http://192.168.1.7:8080/video'
cap.open(adr)

while(True):
            _, frame = cap.read()
            frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            barcodes = pyzbar.decode(gray)
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 10)
                barcodeData = barcode.data.decode("utf-8")
                Product_Id = str(barcodeData)

                #barcodeType = barcode.type
                #text = "{}".format(barcodeData)
                #cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)
                if Quantity(Product_Id) == None:
                    # msg_box("Product Not Found")
                    buttonbox('WARNING Product not FOUND in the database!', image='/home/y/catkin_ws/superstore/notfoundpy.png', choices=['Ok'])
                    cap.open(adr)
                else:
                    if Quantity(Product_Id)<10:
                        play_sound('buzzer1.wav')
                        summary(Product_Id)
                        ans = buttonbox('Shelve out of product !', image='/home/y/catkin_ws/superstore/errorpy.png', choices=['Ok','Exit'])
                        if ans in ['Exit', 'errorpy.png']:
                            cap.release()
                            cv2.destroyAllWindows()
                            break
                        cap.open(adr)

                    else:
                        play_sound('success.wav')
                        ans = buttonbox('Evereything is ok !', image='/home/y/catkin_ws/superstore/okipy.png', choices=['Ok','Exit'])
                        if ans in ['Exit', 'okipy.png']:
                            cap.release()
                            cv2.destroyAllWindows()
                            break
                        cap.open(adr)

            cv2.imshow("QRCODE",frame)
            key = cv2.waitKey(1)
            
cap.release()
cv2.destroyAllWindows()
