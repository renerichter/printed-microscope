# -*- coding: utf-8 -*-
"""
Created on Sat May 28 07:37:45 2016

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
import sys

os.chdir('/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture')
#print (os.getcwd())

def Snapshot():
    camera = picamera.PiCamera()
    try:
        #camera.start_preview()
        #time.sleep(10)
        image_time = datetime.datetime.now()
        camera.capture(str(image_time)+'.jpg')
        #camera.stop_preview()
    finally:
        camera.close()

def VidClip(vidlength):
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        vid_time = datetime.datetime.now()
        camera.start_recording(str(vid_time)+'.h264')
        camera.wait_recording(vidlength)
        camera.stop_recording()
    

from time import sleep

position=[0,0,0]

import RPi.GPIO as GPIO


# Define a function that turns the stepper motors with input parameters
# of the time between steps [seconds], the number of steps to turn,
# and the address of which motor to turn

# For usage, call MotorMove(motor address, steps,delay between steps) 
# For a clockwise rotation, numberofsteps is positive, and for a
# counterclockwise rotation, numberofsteps is negative.

def MotorMove(axis, steps, time_between_steps):
    
    GPIO.setmode(GPIO.BCM)
    
    if axis == 0:
        # Used Pins on the Rapberry Pi
        # This defines the movement for what is labelled as 
        # Motor1, and is functionally the X direction movement.
        A=18
        B=23
        C=24
        D=25
        
    elif axis == 1:
        # Pins used on the Raspberry Pi
        # This defines the movement for what is labelled as
        # Motor2, and is functionally the Z direction movement.
    
        A=4
        B=17
        C=27
        D=22
        
#        A=12
#        B=16
#        C=20
#        D=21
        
    elif axis == 2:
        # Pins used on the Raspberry Pi
        # This defines the movement for what is labelled as 
        # Motor3, and is functionally the Y direction.
#        A=4
#        B=17
#        C=27
#        D=22
        
        A=12
        B=16
        C=20
        D=21

    # Define the pins as GPIO outputs
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)

    # Define steps 1-8 for the stepper motor sequence
    def Step1():
        GPIO.output(D, True)
        sleep (time_between_steps)
        GPIO.output(D, False)

    def Step2():
        GPIO.output(D, True)
        GPIO.output(C, True)
        sleep (time_between_steps)
        GPIO.output(D, False)
        GPIO.output(C, False)

    def Step3():
        GPIO.output(C, True)
        sleep (time_between_steps)
        GPIO.output(C, False)

    def Step4():
        GPIO.output(B, True)
        GPIO.output(C, True)
        sleep (time_between_steps)
        GPIO.output(B, False)
        GPIO.output(C, False)

    def Step5():
        GPIO.output(B, True)
        sleep (time_between_steps)
        GPIO.output(B, False)

    def Step6():
        GPIO.output(A, True)
        GPIO.output(B, True)
        sleep (time_between_steps)
        GPIO.output(A, False)
        GPIO.output(B, False)

    def Step7():
        GPIO.output(A, True)
        sleep (time_between_steps)
        GPIO.output(A, False)

    def Step8():
        GPIO.output(D, True)
        GPIO.output(A, True)
        sleep (time_between_steps)
        GPIO.output(D, False)
        GPIO.output(A, False)
    
#    if max_position[axis]
    
    position_valid = True

    if position_valid == True:     
        
            # Define the step sequence, 1 -> 8 for clockwise
            # 8 -> 1 for counterclockwise, and rotate the
            # appropriate number of steps
        for i in range (abs(steps)):
    
            # Depending on the sign of the number of steps,
            # rotate clockwise or anticlockwise
    
            if steps >= 0:
                # Define a clockwise rotation
                Step1()
                Step2()
                Step3()
                Step4()
                Step5()
                Step6()
                Step7()
                Step8()
                # Update the x position  in the position array
                position[axis] += 1
                # Optionally, print the latest position
                print (position)
                
            if steps < 0:
                # Define an anticlockwise rotation
                Step8()
                Step7()
                Step6()
                Step5()
                Step4()
                Step3()
                Step2()
                Step1()  
                # Update the x position of the position array
                position[axis] -= 1
                # Optionally, print the latest position
                print (position)
                
    GPIO.cleanup()

    return;

"""
This will give some easy commands for running the micrscope
from the command line
"""
while True:
    user_command = input('For help type H. Otherwise, input your command here: ')
    
    if user_command == 'H':

        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PythonPiCamera')      
        
        f = open('help.txt', 'r')
        help_menu = f.read()
        print (help_menu)
        f.close()
        
        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture') 
    
    elif user_command == 'P':
        Snapshot()
    
    elif user_command == 'V':
        vid_length = int(input('Enter video length in seconds: '))
        VidClip(vid_length)
        
    elif user_command == 'X':
        sys.exit(0)
        
    elif user_command == 'A':
        MotorMove(0,-10,0.001)
        
    elif user_command == 'D':
        MotorMove(0,10,0.001)
        
    elif user_command == 'W':
        MotorMove(1,10,0.001)
                
    elif user_command == 'S':
        MotorMove(1,-10,0.001)
        
    elif user_command == 'AA':
        MotorMove(0,-100,0.001)
        
    elif user_command == 'DD':
        MotorMove(0,100,0.001)
        
    elif user_command == 'WW':
        MotorMove(1,100,0.001)
                
    elif user_command == 'SS':
        MotorMove(1,-100,0.001)
        
    elif user_command == 'Q':
        MotorMove(2,10,0.001)
        
    elif user_command == 'E':
        MotorMove(2,-10,0.001)
        
#MotorMove(2,-200,0.001)
#time.sleep(1)
#Snapshot()


#for num in range(0,5):
#    time.sleep(1)        
#    Snapshot()
#    MotorMove(1,50,0.001)


#MotorMove(0,-2000,0.001)
#MotorMove(0,-1000,0.001)

#MotorMove(1,-2000,0.001)
#MotorMove(1,-1000,0.001)

#MotorMove(2,1000,0.001)
#MotorMove(2,2000,0.001)

#VidClip(1)
