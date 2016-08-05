# -*- coding: utf-8 -*-
"""
Created on Sat May 28 12:26:50 2016

@author: pi
"""

"""
Take a preview from the PiCam and display it.
Use this to see how the motor control is working
"""

import time  
import os
import picamera
import datetime

#print (os.getcwd())
os.chdir('/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture')
print (os.getcwd())


def Snapshot():
    camera = picamera.PiCamera()
    try:
        #camera.start_preview()
        #time.sleep(10)
        current_time = datetime.datetime.now()
        camera.capture(str(current_time)+'.jpg')
        #camera.stop_preview()
    finally:
        camera.close()