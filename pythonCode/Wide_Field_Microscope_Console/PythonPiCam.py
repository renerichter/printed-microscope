# -*- coding: utf-8 -*-
"""
Created on August 4th 2016

@author: Scott Strachan, IPHT Mikroskopie Gruppe
"""

"""
This program provides control over the 3D printed microscope through
interaction with the command line.

Functionality includes:

- Ability to move in x, y, and z directions in predefined step sizes
- Ability to redefine these steps sizes, as well as change the speed
    at which the motors rotate.
- Limits on the range of the stepper motors to avoid damaging the 
    microscope
- Saves the last position of the stepper motors upon graceful shutdown,
    and upon every motor movement.
- Loads last saved position upon launch of the program
- Typing H provides a simple help menu summarizing functions
- Take a simple time stamped image
- Take a simple time stamped video of a given length in seconds
- Change the self directory (where the relevant text files
    are located), and the save directory, where the image and video files
    are stored.
- Change the image resolution through a "camera settings" menu
- Show a preview of the current scene in the image plane
- Change the length of the preview through the "camera settings" menu
- Display the contents of relevant menu text files to provide helpful 
    information about how to navigate the settings menus
- Allow the user to save a temporary position that can be returned to at a 
    later time. Currently done by number of steps away from saved point.
    If the SavePosition() has not been called yet, the motors will return to
    the positions where they were at the launch of the program.
- Allow the user to return to the origin
- Allow the user to move to an arbitrarily defined position, given that it is 
    within the allowable range of the motors.
- Allow the user to set the "small" and "large" steps sizes, as well as change
    the time_pause between steps, controlling the rotation speed of the motors.
- Allow the user to take a one dimensional scan in a given direction while
    taking images at a predefined interval, or change the spacing to give a 
    predefined number of images.

"""


# Import required libraries

import os
import picamera
import datetime
import sys
from time import sleep 
import RPi.GPIO as GPIO
import time

# Initialize the directory appropriately such that the program can find the
# associated text files for the menus and the saved position.

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
# file. It will print the saved values to the console window. Currently commented
# out because it is not being called anywhere else.

#def ReadPositionFile():
#        os.chdir(directory_self)
#        f = open('saved_position.txt', 'r')
#        saved_values = f.read()
#        print (saved_values)
#        f.close()
#        os.chdir(directory_save)

# This function sets the position array to the values that are saved in the
# saved_positions.txt file.

def SetPositionFromFile():
        os.chdir(directory_self)
        r = open('saved_position.txt', 'r')
        lines = r.readlines()
        for i in range(0,3):
            position[i] = int(lines[i].strip('\n'))
        os.chdir(directory_save)
        
# This function displays the contents of a text file to the screen. It is
# used to display the various menus used by the program that are stored in
# text files in the directory_self.

def DisplayMenu(menu_name):
        os.chdir(directory_self)      
        f = open(str(menu_name), 'r')
        menu = f.read()
        print (menu)
        f.close()
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

# Give an initial definition of what constitutes a "small" and a "large" step
# for the stepper motor control, as well as the default time between steps

small_step_size = 10
large_step_size = 100
step_pause = 0.001

# Define a dictionary to map x, y, and z to the motor address points 0, 1, and 2.
# Also define the dictionary in the other way, so that x, y, and z can be returned
# from the indices 0, 1, and 2.

def createMotorDictionary(): 
    motor_dict = dict()
    motor_dict['x'] = 0
    motor_dict['y'] = 1
    motor_dict['z'] = 2
    motor_dict['X'] = 0
    motor_dict['Y'] = 1
    motor_dict['Z'] = 2
    motor_dict[0] = 'x'
    motor_dict[1] = 'y'
    motor_dict[2] = 'z'
    return motor_dict

# Immediately launch this dictionary to be able to use it at a later time.

motorMap = createMotorDictionary()

# Define a function that simply prints the latest value of the position array
# to the console. Also define a function that prints the currently saved
# position.

def PrintPosition():
    print ('Latest position: ' + str(position))
        
def PrintSavedPosition():
    print ('Saved postion: ' + str(temp_position))
        
# Define a function that saves the current position to the temp_position array.
# Define a function that returns the stepper motors to the saved position.
# Define a function that returns the stepper motors to the origin.

        
def SavePosition():
    for y in range(0,3):
        temp_position[y] = position[y]
    PrintSavedPosition()
        
def ReturnToSavedPosition():
    for x in range(0,3):
        MotorMove(x,(temp_position[x] - position[x]),step_pause)
    
def ReturnToOrigin():
    for x in range(0,3):
        MotorMove(x,(-position[x]),step_pause)

# Define a function that moves the stepper motors to an arbitrary position, but
# only if the new position is within the allowable range of the stepper motors.
        
def MoveToPosition(new_position):

    # Define a series of booleans to keep track of whether or not the movement
    # is allowable. move_to_position_valid is a boolean that ensures that all
    # three directions are allowable before allowing any motion of the motors.
    # Initialized to false to prevent unwanted movement.

    new_move_valid_x = False
    new_move_valid_y = False
    new_move_valid_z = False
    move_to_position_valid = False
    
    # Check that each of the new position values is within the maximum allowable
    # positions.
    
    if abs(new_position[0]) < max_position[0]:
            new_move_valid_x = True
    else:
            new_move_valid_x = False   
            
    if abs(new_position[1]) < max_position[1]:
            new_move_valid_y = True
    else:
            new_move_valid_y = False 

    if abs(new_position[2]) < max_position[2]:
            new_move_valid_z = True
    else:
            new_move_valid_z = False             
    
    # Ensure that all three requested movements are allowable before moving any
    # of the motors. This is done by setting the move_to_position_valid boolean.
    
    if new_move_valid_x == True and new_move_valid_y == True and new_move_valid_z == True:
        print ('Movement allowed.')
        move_to_position_valid = True
    else:
        print ('Movement not allowed.')
        move_to_position_valid = False
    
    # If the movement is allowed, move to the new position and print the latest
    # position. Otherwise, inform the user that he/she needs to select a new
    # desired position.
    
    if move_to_position_valid == True:
        for x in range(0,3):
            MotorMove(x,(new_position[x]-position[x]),step_pause)
        PrintPosition()
    else:
        print ('Select a new position within the allowable boundaries.')
        
def UserDefinedPosition():

    user_new_position = [0,0,0]
    user_new_position[0] = int(input('New x position: '))
    user_new_position[1] = int(input('New y position: '))        
    user_new_position[2] = int(input('New z position: '))        
    MoveToPosition(user_new_position)
        
# Save the initial position at the launch of the program to the temp_position array.

SavePosition()

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

def OneDimensionalScan(direction,scan_min_value,scan_max_value):
    print ('You\'ve selected' + str(direction) + 'scan. Showing a preview of your image region...')
    sleep (2)
    Preview(3)
    sleep (1)
    centered_target = str(input('Is your image target centered in the screen? (Y or N): '))
    if centered_target == 'Y':
        z_max = int(input('Please enter the maximum desired z position of the scan: '))
        z_min = int(input('Please enter the minumum desired z position of the scan: '))
            
        if z_max <= z_min:
            print ('Please ensure that the maximum z value is greater than the minimum z value and try again.')
        else:
            print ('Do you want to define the number of images in the z scan (N), or the spacing between each image (S)?')
            
        zscan_method = str(input('Enter your choice here: '))
        
        if zscan_method == 'N':
            number_of_images = int(input('Enter the number of images in the z scan: '))                    
            MoveToPosition([position[0],position[1],z_min])
            for x in range(0,number_of_images): 
                MotorMove(2,int((z_max-z_min)/number_of_images),step_pause)
                sleep (1)
                Snapshot()
                PrintPosition()
        elif zscan_method == 'S':
            MoveToPosition([position[0],position[1],z_min])                    
            print ('Not finished yet')
                    
    elif centered_target == 'N':
        print ('Ensure that your image target is centered in the screen before trying the z scan again.')
    else:
        print ('No valid option selected.')

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
        DisplayMenu('help.txt')
    
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
    
    # The following six commands give movement in  steps of small_step_size
    # stepper motor steps in both directions of the x, y, and z travel directions.
    # Move at a speed of rotation according to the value of step_pause.
    
    elif user_command == 'A':          
        MotorMove(0,-small_step_size,step_pause)         
        PrintPosition()
        UpdatePositionFile()
        
    elif user_command == 'D':
        MotorMove(0,small_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
        
    elif user_command == 'S':
        MotorMove(1,small_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
                
    elif user_command == 'W':
        MotorMove(1,-small_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
    
    elif user_command == 'Q':
        MotorMove(2,-small_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
        
    elif user_command == 'E':
        MotorMove(2,small_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
    
    # The following six commands give movement in steps of large_step_size stepper
    # motor steps in both directions of the x, y, and z travel directions.
    # Move at a speed of rotation according to the value of step_pause.
    
    elif user_command == 'AA':
        MotorMove(0,-large_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
        
    elif user_command == 'DD':
        MotorMove(0,large_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
        
    elif user_command == 'SS':
        MotorMove(1,large_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
                
    elif user_command == 'WW':
        MotorMove(1,-large_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
        
    elif user_command == 'QQ':
        MotorMove(2,-large_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
        
    elif user_command == 'EE':
        MotorMove(2,large_step_size,step_pause)
        PrintPosition()
        UpdatePositionFile()
    
    # Allow the user to temporarily save a position that can be returned to
    # later with a single command. Use N to save the current position to the
    # temp_position array, and use M to return to that saved position at any
    # later time. Also provide a function for returning to the origin at any
    # time. Finally, provide the user a way to see what the currently saved
    # position is.
    
    elif user_command == 'N':
        SavePosition()
        PrintSavedPosition()

    elif user_command == 'M':
        ReturnToSavedPosition()
        PrintPosition()
        
    elif user_command == 'B':
        ReturnToOrigin()
        PrintPosition()
        
    elif user_command == 'K':
        PrintSavedPosition()
    
    elif user_command == 'R':
        UserDefinedPosition()
        
    # The following commands can be used to perform an automated scan through
    # z while taking images at constant intervals. This can be used to
    # calibrate the microscope, or to get a series of images through the z plane
    
    elif user_command == 'O':
        user_direction = str(input('Enter the desired scan direction: '))
        desired_min_scan = int(input('Enter the desired starting position: '))
        desired_max_scan = int(input('Enter the desired ending position: '))
        OneDimensionalScan(user_direction,desired_min_scan,desired_max_scan)
            
    # The following commands can be used to change the self and save
    # directories. The self directory keeps the help.txt and saved_positions.txt
    # files which are required for the program to run properly.
    # The save directory determines where the image and video files are saved.
    
    elif user_command == 'G':
        DisplayMenu('directory_menu.txt')        
        directory_menu = str(input('Enter your choice here: '))
        if directory_menu == 'R':
            directory_self = str(input('Enter the new self directory here: '))
        elif directory_menu == 'T':
            directory_save = str(input('Enter the new save directory here: '))
        else:
            directory_self = directory_self
            directory_save = directory_save
            
    # This entry will allow the user to customize the number of steps that are
    # defined in the "small" and "large" steps used by the stepper motors.
    # It also allows the user to specify the time pause between steps in the
    # stepper motor control sequence. A shorter time pause corresponds to a
    # faster rotation of the stepper motors. The input for the time pause
    # is given in milliseconds.
    
    elif user_command == 'J':
        
        # Find the motor_menu.txt file and display the contents        
        DisplayMenu('motor_menu.txt') 
        
        motor_menu_choice = str(input("Enter your choice here: "))
        if motor_menu_choice == 'S':
            small_step_size = int(input("Enter the new desired small step size. Must be an integer: "))
        elif motor_menu_choice == 'L':
            large_step_size = int(input("Enter the new desired large step size. Must be an integer: "))
        elif motor_menu_choice == 'T':
            desired_step_pause = int(input("Enter the new pause between steps (must be an integer between 1 & 100): "))
            if desired_step_pause >= 1 and desired_step_pause <= 100:
                step_pause = desired_step_pause/1000
            else:
                print ("Invalid pause between steps.")
        else:
            small_step_size = small_step_size
            large_step_size = large_step_size
            step_pause = step_pause
    
    # This part controls the camera settings menu. There's another txt file,
    # camera_menu.txt that outlines what the options are.
    elif user_command == 'C':
        
        # Find the camera_menu.txt file and display the contents        
        DisplayMenu('camera_menu.txt')
        
        # Prompt the user for an option in the camera menu
        camera_menu_choice = str(input('Enter your choice here: '))
        
        # If the user wants to change the image resolution        
        if camera_menu_choice == 'R':
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
        if camera_menu_choice == 'T':
            new_preview_length = int(input('Please enter the new preview length in seconds: '))
            preview_length = new_preview_length