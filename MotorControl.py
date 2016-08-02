# -*- coding: utf-8 -*-


# Define and initialize an array to keep track of the
# position of the motors
# The array is in the format of [x, y, z] in numbers of steps

position=[0,0,0]

# Define a function that turns motor 1 with input parameters
# of the time between steps [seconds] and the
# number of steps to turn

# For usage, call motor_1 with arguments for the time delay
# between steps and then the number of steps to turn. For a
# clockwise rotation, numberofsteps is positive, and for a
# counterclockwise rotation, numberofsteps is negative

def motor_1(steptime,numberofsteps): 

    from time import sleep
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    # Used Pins on the Rapberry Pi
    A=18
    B=23
    C=24
    D=25
    time = steptime

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
        sleep (time)
        GPIO.output(D, False)

    def Step2():
        GPIO.output(D, True)
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(D, False)
        GPIO.output(C, False)

    def Step3():
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(C, False)

    def Step4():
        GPIO.output(B, True)
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(B, False)
        GPIO.output(C, False)

    def Step5():
        GPIO.output(B, True)
        sleep (time)
        GPIO.output(B, False)

    def Step6():
        GPIO.output(A, True)
        GPIO.output(B, True)
        sleep (time)
        GPIO.output(A, False)
        GPIO.output(B, False)

    def Step7():
        GPIO.output(A, True)
        sleep (time)
        GPIO.output(A, False)

    def Step8():
        GPIO.output(D, True)
        GPIO.output(A, True)
        sleep (time)
        GPIO.output(D, False)
        GPIO.output(A, False)

    # Define the step sequence, 1 -> 8 for clockwise
    # 8 -> 1 for counterclockwise, and rotate the
    # appropriate number of steps

    for i in range (abs(numberofsteps)):

        # Depending on the sign of the number of steps,
        # rotate clockwise or anticlockwise

        if numberofsteps >= 0:
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
            position[0] += 1
            # Optionally, print the latest position
            print position
            
        if numberofsteps < 0:
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
            position[0] -= 1
            # Optionally, print the latest position
            print position
    GPIO.cleanup()

    return;

# Define a function that turns motor 2 with input parameters
# of the time between steps [seconds] and the
# number of steps to turn

# For usage, call motor_2 with arguments for the time delay
# between steps and then the number of steps to turn. For a
# clockwise rotation, numberofsteps is positive, and for a
# counterclockwise rotation, numberofsteps is negative# Same exact code as given for motor_1. Same usage and
# method, simply using a different set of pins to control
# a different motor

def motor_2(steptime,numberofsteps): 

    from time import sleep
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    # Pins used on the Raspberry Pi
    A=12
    B=16
    C=20
    D=21
    time = steptime

    # Define the pins as GPIO outputs
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)

    # Define steps 1-8
    def Step1():
        GPIO.output(D, True)
        sleep (time)
        GPIO.output(D, False)

    def Step2():
        GPIO.output(D, True)
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(D, False)
        GPIO.output(C, False)

    def Step3():
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(C, False)

    def Step4():
        GPIO.output(B, True)
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(B, False)
        GPIO.output(C, False)

    def Step5():
        GPIO.output(B, True)
        sleep (time)
        GPIO.output(B, False)

    def Step6():
        GPIO.output(A, True)
        GPIO.output(B, True)
        sleep (time)
        GPIO.output(A, False)
        GPIO.output(B, False)

    def Step7():
        GPIO.output(A, True)
        sleep (time)
        GPIO.output(A, False)

    def Step8():
        GPIO.output(D, True)
        GPIO.output(A, True)
        sleep (time)
        GPIO.output(D, False)
        GPIO.output(A, False)

    # Define the step sequence, 1 -> 8 for clockwise
    # 8 -> 1 for counterclockwise, and rotate the
    # appropriate number of steps

    
    for i in range (abs(numberofsteps)):

        # Depending on the sign of the number of steps,
        # rotate clockwise or anticlockwise

        if numberofsteps >= 0:
            # Define a clockwise rotation
            Step1()
            Step2()
            Step3()
            Step4()
            Step5()
            Step6()
            Step7()
            Step8()  
            # Update the y position in the position array
            position[1] += 1
            # Optionally, print the updated position
            print position
            
        if numberofsteps < 0:
            # Define an anticlockwise rotation
            Step8()
            Step7()
            Step6()
            Step5()
            Step4()
            Step3()
            Step2()
            Step1()  
            # Update the y position in the position array
            position[1] -= 1
            # Optionally, print the updated position
            print position
    GPIO.cleanup()

    return;

# Define a function that turns motor 3 with input parameters
# of the time between steps [seconds] and the
# number of steps to turn

# For usage, call motor_3 with arguments for the time delay
# between steps and then the number of steps to turn. For a
# clockwise rotation, numberofsteps is positive, and for a
# counterclockwise rotation, numberofsteps is negative# Same exact code as given for motor_1. Same usage and
# method, simply using a different set of pins to control
# a different motor

def motor_3(steptime,numberofsteps):

    from time import sleep
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    # Pins used on the Raspberry Pi
    A=4
    B=17
    C=27
    D=22
    time = steptime

    # Define the pins as GPIO outputs
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)

    # Define steps 1-8
    def Step1():
        GPIO.output(D, True)
        sleep (time)
        GPIO.output(D, False)

    def Step2():
        GPIO.output(D, True)
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(D, False)
        GPIO.output(C, False)

    def Step3():
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(C, False)

    def Step4():
        GPIO.output(B, True)
        GPIO.output(C, True)
        sleep (time)
        GPIO.output(B, False)
        GPIO.output(C, False)

    def Step5():
        GPIO.output(B, True)
        sleep (time)
        GPIO.output(B, False)

    def Step6():
        GPIO.output(A, True)
        GPIO.output(B, True)
        sleep (time)
        GPIO.output(A, False)
        GPIO.output(B, False)

    def Step7():
        GPIO.output(A, True)
        sleep (time)
        GPIO.output(A, False)

    def Step8():
        GPIO.output(D, True)
        GPIO.output(A, True)
        sleep (time)
        GPIO.output(D, False)
        GPIO.output(A, False)

    # Define the step sequence, 1 -> 8 for clockwise
    # 8 -> 1 for counterclockwise, and rotate the
    # appropriate number of steps    
    for i in range (abs(numberofsteps)):

        # Depending on the sign of the number of steps,
        # rotate clockwise or anticlockwise

        if numberofsteps >= 0:
            # Define a clockwise rotation
            Step1()
            Step2()
            Step3()
            Step4()
            Step5()
            Step6()
            Step7()
            Step8()  
            # Update the z position in the position array
            position[2] += 1
            # Optionally, print the updated position array
            print position
            
        if numberofsteps < 0:
            # Define an anticlockwise rotation
            Step8()
            Step7()
            Step6()
            Step5()
            Step4()
            Step3()
            Step2()
            Step1()  
            # Update the z position in the position array
            position[2] -= 1
            # Optionally, print the updated position array
            print position
    GPIO.cleanup()

    return;

# Import time to be able to stop the process for a defined
# amount of time

import time

# Define a function that scans through an xy plane at an
# arbitrary position in z.

def xy_scan(xmax,ymax,xspeed,yspeed):

    # Define some local variables to keep track of how far
    # the motors have scanned

    x = 0;
    y = 0;
    
    #Stop movement to allow things to settle
    
    time.sleep(0.1); 


    # MIGHT NEED TO GENERALIZE TO INCLUDE ARBITRARILY LARGE
    # STEPS BETWEEN EACH SCANNED ROW

    # For all values of y less than the defined maximum y
    # range, scan through in x from the starting x position
    # through to the defined x maximum and then return
    
    while y <= ymax:
            motor_1(xspeed,xmax);
            motor_2(yspeed,1);
            y += 1;
            if y <= ymax:
                motor_1(xspeed,-xmax);
                motor_2(yspeed,1);
                y += 1;

    return;
    

# Define a function that scans through an entire xyz region

def xyz_scan(xstart,ystart,zstart,xmax,ymax,zmax,xspeed,yspeed,zspeed):

    # Move to the initial position
    
    motor_1(0.001,xstart);
    motor_2(0.001,ystart);
    motor_3(0.001,zstart);

    # Define a local variable to keep track of the z position
    
    z = 0;

    # Scan through the defined xmax, ymax range at each z
    # position within the defined zmax range
    
    while z < zmax:
        xy_scan(xmax,ymax,xspeed,yspeed)
        motor_3(zspeed,1);
        z += 1;
        if position[0] >= xmax:
            motor_1(xspeed,-xmax-1);
        if position[1] >= ymax:
            motor_2(yspeed,-ymax-1);
            
    return;

#xy_scan(19,24,0.001,0.001)
xyz_scan(0,0,0,10,10,4,0.001,0.001,0.001)

