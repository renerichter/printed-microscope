# -*- coding: utf-8 -*-
"""
Created on Sat May 28 07:37:45 2016

@author: pi
"""

"""
This program provides control over the 3D printed microscope through
interaction with the command line.

Functionality includes:

- Ability to move in x, y, and z directions in predefined step sizes
- Limits on the range of the stepper motors to avoid damaging the 
    microscope
- Saves the last position of the stepper motors upon graceful shutdown
- Loads last saved position upon launch of the program
- H provides a simple help menu summarizing functions
- Take a simple time stamped image
- Take a simple time stamped video of a given length in seconds

"""


# Import required libraries

import os
import picamera
import datetime
import sys
from time import sleep 
import RPi.GPIO as GPIO

# Set the directory appropriately such that the program can find the
# associated text files for the help menu and the saved position.

os.chdir('/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture')

# Define the function that will take a simple image and save it to the 
# defined save directory with a file name that is the timestamp 
# at which the image was taken.

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

# Define the function that will take a simple video and save it to the
# defined save directory with a file name that is the timestamp at which
# the video was taken. 
# Need to prompt the user for the desired video length in seconds.

def VidClip(vidlength):
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        vid_time = datetime.datetime.now()
        camera.start_recording(str(vid_time)+'.h264')
        camera.wait_recording(vidlength)
        camera.stop_recording()

# This is the function that opens the saved_position.txt file, and writes
# the latest position to the file. This saved file is used to keep track of
# the position of the microscope stage even after the program is shutdown.
# This ensures that the position never goes beyond the maximum allowable 
# position.

def UpdatePositionFile():
        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PythonPiCamera')        
        w = open('saved_position.txt', 'w')
        w.write(str(position[0]) + '\n')
        w.write(str(position[1]) + '\n')
        w.write(str(position[2]))
        w.close()
        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture')

# This function reads the position that is saved in the saved_positions.txt 
# file. It will print the saved values to the console window.

def ReadPositionFile():
        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PythonPiCamera')
        f = open('saved_position.txt', 'r')
        saved_values = f.read()
        print (saved_values)
        f.close()
        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture')

# This function sets the position array to the values that are saved in the
# saved_positions.txt file.

def SetPositionFromFile():
        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PythonPiCamera')
        r = open('saved_position.txt', 'r')
        lines = r.readlines()
        for i in range(0,3):
            position[i] = int(lines[i].strip('\n'))
        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture')

# Initialize the position array, set the values of this array from the saved
# file, saved_positions.txt, and finally define the maximum allowable position
# in terms of number of steps for the motors, to prevent the stage from 
# going beyond its allowable range.

position = [0,0,0]
SetPositionFromFile() 
max_position = [2000,2000,2000]

# Define a function that simply prints the latest value of the position array
# to the console.

def PrintPosition():
        print ('Latest position: ' + str(position))


"""

Define a function that turns the stepper motors with input parameters
of the address of which motor to turn, the number of steps to turn, 
and the time between steps [seconds].

For usage, call MotorMove(motor address, steps, delay between steps) 
For a clockwise rotation, numberofsteps is positive, and for a
counterclockwise rotation, numberofsteps is negative.

The motors are addressed as 0 - x axis, 1 - y axis, and 2 - z axis

There are 512 steps in a full rotation, and the smallest time delay between
steps (which corresponds to the fastest movement) is 0.001 secodns, or 1 ms.

A longer time between steps corresponds to a slower average motor movement.

""" 


def MotorMove(axis, steps, time_between_steps):
    
    GPIO.setmode(GPIO.BCM)
    
    if axis == 0:
        # Used Pins on the Rapberry Pi
        # This defines the movement for what is labelled as 
        # M1 on the motor itself, and is functionally the 
        # X direction movement.
        A=18
        B=23
        C=24
        D=25
        
    elif axis == 1:
        # Pins used on the Raspberry Pi
        # This defines the movement for what is labelled as
        # M3 on the motor itslef, and is functionally the 
        # Y direction movement.
    
        A=4
        B=17
        C=27
        D=22
        
        
    elif axis == 2:
        # Pins used on the Raspberry Pi
        # This defines the movement for what is labelled as 
        # M2 on the motor itslef, and is functionally the 
        # Z direction.
        
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
    
    
    # This is a check to see if the proposed motor movement would move
    # the stepper motor outside of the allowable range. This is to
    # prevent the motor from destroying the microscope by simply until 
    # the nut becomes loose, or the interior post hits the gearing mechanism
    
    if max_position[axis] > abs(position[axis] + steps):
        position_valid = True
    else:
        position_valid = False
    
    # If the proposed position is valid, rotate the motor until the 
    # new position is reached 
    
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
                # Update the position array
                position[axis] += 1
                
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
                # Update the position array
                position[axis] -= 1
    
    # If the proposed position is invalid, give the user a short error message.
    
    else:
        print ("End of stage range. Try using a smaller step or going in another direction")
        
    GPIO.cleanup()

    return;


"""

This will give some easy commands for running the micrscope
from the command line. This control menu will be continuously running
until the user decides to exit the menu. The full functionality of the 
control program is implemented here.

"""


while True:
    
    # Prompt the user for a command.
    
    user_command = input('For help type H. Otherwise, input your command here: ')
    
    # If the help menu is requested, change directories to find the correct
    # file, open the file, read the file, display the file, and close the file.
    # Finally, change the directory back to the appropriate save directory.
    
    if user_command == 'H':

        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PythonPiCamera')      
        
        f = open('help.txt', 'r')
        help_menu = f.read()
        print (help_menu)
        f.close()
        
        os.chdir('/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture') 
    
    # If a picture is requested call the Snapshot() function
    
    elif user_command == 'P':
        Snapshot()
    
    # If a video is requested, prompt the user for the length of the video
    # Then call the VidClip(vidlength) function.
    
    elif user_command == 'V':
        requested_vidlength = int(input('Enter video length in seconds: '))
        VidClip(requested_vidlength)
    
    # Before exiting the program, save the current position of the microscope
    # stage to the position file.
    
    elif user_command == 'X':
        UpdatePositionFile()        
        sys.exit(0)
    
    # The following six commands give movement in small steps of 10 stepper
    # motor steps in both directions of the x, y, and z travel directions.
    
    elif user_command == 'A':
        MotorMove(0,-10,0.001)
        PrintPosition()
        
    elif user_command == 'D':
        MotorMove(0,10,0.001)
        PrintPosition()
        
    elif user_command == 'S':
        MotorMove(1,10,0.001)
        PrintPosition()
                
    elif user_command == 'W':
        MotorMove(1,-10,0.001)
        PrintPosition()
    
    elif user_command == 'Q':
        MotorMove(2,-10,0.001)
        PrintPosition()
        
    elif user_command == 'E':
        MotorMove(2,10,0.001)
        PrintPosition()
    
    # The following six commands give movement in large steps of 100 stepper
    # motor steps in both directions of the x, y, and z travel directions.
    
    elif user_command == 'AA':
        MotorMove(0,-100,0.001)
        PrintPosition()
        
    elif user_command == 'DD':
        MotorMove(0,100,0.001)
        PrintPosition()
        
    elif user_command == 'SS':
        MotorMove(1,100,0.001)
        PrintPosition()
                
    elif user_command == 'WW':
        MotorMove(1,-100,0.001)
        PrintPosition()
        
    elif user_command == 'QQ':
        MotorMove(2,-100,0.001)
        PrintPosition()
        
    elif user_command == 'EE':
        MotorMove(2,100,0.001)
        PrintPosition()
