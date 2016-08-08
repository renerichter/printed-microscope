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
- Change the self directory (where the help.txt and saved_position.txt files
    are located) and the save directory, where the image and video files
    are stored.
- Change the image resolution through a "camera settings" menu
- Show a preview of the current scene in the image plane
- Change the length of the preview through the "camera settings" menu
- Display the contents of camera_settings.txt to provide helpful information
    about how to navigate the camera settings menu
- Allow the user to save a temporary position that can be returned to at a 
    later time. Currently done by number of steps away from saved point.
    If this functionality is called at program launch, the microscope stage
    will return to the origin.

"""


# Import required libraries

import os
import picamera
import datetime
import sys
from time import sleep 
import RPi.GPIO as GPIO
import time
import operator

# Initialize the directory appropriately such that the program can find the
# associated text files for the help menu and the saved position.

directory_self = "/home/pi/Documents/3D Printed Microscope Project/PythonPiCamera"
directory_save = "/home/pi/Documents/3D Printed Microscope Project/PiCamImageCapture"

os.chdir(directory_save)

# Initialize some camera settings

camera_resolution = (640,480)
preview_length = 3

# Define the function that will take a simple image and save it to the 
# defined save directory with a file name that is the timestamp 
# at which the image was taken.

def Snapshot():
    os.chdir(directory_save)    
    camera = picamera.PiCamera()
    try:
        camera.resolution = camera_resolution
        image_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        camera.capture(str(image_time)+'.jpg')
    finally:
        camera.close()

# Define the function that will take a simple video and save it to the
# defined save directory with a file name that is the timestamp at which
# the video was taken. 
# Need to prompt the user for the desired video length in seconds.

def VidClip(vidlength):
    os.chdir(directory_save)
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        vid_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        camera.start_recording(str(vid_time)+'.h264')
        camera.wait_recording(vidlength)
        camera.stop_recording()

# Define a function that will display a preview of what is in the image plane.
# Takes an argument that defines the length of the preview.

def Preview(length):
    camera = picamera.PiCamera()
    try:
        camera.resolution = camera_resolution
        camera.start_preview()
        time.sleep(length)
        camera.stop_preview()
    finally:
        camera.close()

# This is the function that opens the saved_position.txt file, and writes
# the latest position to the file. This saved file is used to keep track of
# the position of the microscope stage even after the program is shutdown.
# This ensures that the position never goes beyond the maximum allowable 
# position.

def UpdatePositionFile():
        os.chdir(directory_self)        
        w = open('saved_position.txt', 'w')
        w.write(str(position[0]) + '\n')
        w.write(str(position[1]) + '\n')
        w.write(str(position[2]))
        w.close()
        os.chdir(directory_save)

# This function reads the position that is saved in the saved_positions.txt 
# file. It will print the saved values to the console window.

def ReadPositionFile():
        os.chdir(directory_self)
        f = open('saved_position.txt', 'r')
        saved_values = f.read()
        print (saved_values)
        f.close()
        os.chdir(directory_save)

# This function sets the position array to the values that are saved in the
# saved_positions.txt file.

def SetPositionFromFile():
        os.chdir(directory_self)
        r = open('saved_position.txt', 'r')
        lines = r.readlines()
        for i in range(0,3):
            position[i] = int(lines[i].strip('\n'))
        os.chdir(directory_save)

# Initialize the position array, set the values of this array from the saved
# file, saved_positions.txt, and finally define the maximum allowable position
# in terms of number of steps for the motors, to prevent the stage from 
# going beyond its allowable range.

position = [0,0,0]
SetPositionFromFile() 
max_position = [2000,2000,2000]

# Set a temporary position that is used for saving locations that the user
# wants to return to at a later time

temp_position = [0,0,0]

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

        os.chdir(directory_self)      
        
        f = open('help.txt', 'r')
        help_menu = f.read()
        print (help_menu)
        f.close()
        
        os.chdir(directory_save) 
    
    # If a picture is requested call the Snapshot() function
    
    elif user_command == 'P':
        Snapshot()
    
    # If a preview is requested call the Preview(length) function
    
    elif user_command == 'T':
        Preview(preview_length)
    
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
    
    # Allow the user to temporarily save a position that can be returned to
    # later with a single command. Use N to save the current position to the
    # temp_position array, and use M to return to that saved position at any
    # later time.
    
    elif user_command == 'N':
        for y in range(0,3):
            temp_position[y] = position[y]

    elif user_command == 'M':
        for x in range(0,3):
            MotorMove(x,(temp_position[x] - position[x]),0.001)

        print (position)
        
    # The following commands can be used to change the self and save
    # directories. The self directory keeps the help.txt and saved_positions.txt
    # files which are required for the program to run properly.
    # The save directory determines where the image and video files are saved.
    
    elif user_command == 'G':
        directory_menu = str(input('Type \'R\' to change the self directory and \'T\' to change the save directory. Any other entry will exit this menu.\nEnter your option here: '))
        if directory_menu == 'R':
            directory_self = str(input('Enter the new self directory here: '))
        elif directory_menu == 'T':
            directory_save = str(input('Enter the new save directory here: '))
        else:
            directory_self = directory_self
            directory_save = directory_save
    
    # This part controls the camera settings menu. There's another txt file,
    # camera_menu.txt that outlines what the options are.
    elif user_command == 'C':
        
        # Find the camera_menu.txt file and display the contents        
        os.chdir(directory_self)      
        
        f = open('camera_menu.txt', 'r')
        help_menu = f.read()
        print (help_menu)
        f.close()
        os.chdir(directory_save) 
        
        # Prompt the user for an option in the camera menu
        camera_settings_menu = str(input('Enter your choice here: '))
        
        # If the user wants to change the image resolution        
        if camera_settings_menu == 'R':
            # Give the user three options for images, corresponding to the
            # three built in image resolutions for the camera.
            print ('L - 2592 x 1944 \nM - 1296 x 972 \nS - 640 x 480 \nAny other key - exit')            
            
            # Change the resolution accordingly.
            new_resolution = input('Change the image resolution: ')           
            if new_resolution == 'L':
                camera_resolution = (2592,1944)
            elif new_resolution == 'M':
                camera_resolution = (1296,972)
            elif new_resolution == 'S':
                camera_resolution = (640,480)
            else:
                camera_resolution = camera_resolution
        
        # Allow for the preview length to be adjustable
        if camera_settings_menu == 'T':
            new_preview_length = int(input('Please enter the new preview length in seconds: '))
            preview_length = new_preview_length
        