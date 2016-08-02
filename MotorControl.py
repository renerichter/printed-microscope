# -*- coding: utf-8 -*-

position=[0,0,0]

def motor1(steptime,numberofsteps): 

    from time import sleep
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    # Verwendete Pins am Rapberry Pi
    A=18
    B=23
    C=24
    D=25
    time = steptime

    # Pins als Ausgänge definieren
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)

    # Schritte 1 - 8 festlegen
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

    # Step sequence defined over a number of steps    
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
            # Update the position array
            position[0] += 1
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
            # Update the position array
            position[0] -= 1
            print position
    GPIO.cleanup()

    return;


def motor2(steptime,numberofsteps): 

    from time import sleep
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    # Verwendete Pins am Rapberry Pi
    A=12
    B=16
    C=20
    D=21
    time = steptime

    # Pins als Ausgänge definieren
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)

    # Schritte 1 - 8 festlegen
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

    # Step sequence defined over a number of steps    
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
            # Update the position array
            position[1] += 1
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
            # Update the position array
            position[1] -= 1
            print position
    GPIO.cleanup()

    return;

def motor3(steptime,numberofsteps):

    from time import sleep
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    # Verwendete Pins am Rapberry Pi
    A=4
    B=17
    C=27
    D=22
    time = steptime

    # Pins als Ausgänge definieren
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)

    # Schritte 1 - 8 festlegen
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

    # Step sequence defined over a number of steps    
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
            # Update the position array
            position[2] += 1
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
            # Update the position array
            position[2] -= 1
            print position
    GPIO.cleanup()

    return;

import time
def scan(xstart,ystart,zstart,xmax,ymax,zmax,xspeed,yspeed,zspeed):
    x = 0;
    y = 0;
    z = 0;

    #Move to the initial position
    motor1(0.001,xstart);
    motor2(0.001,ystart);
    motor3(0.001,zstart);
    #Stop movement to allow things to settle
    time.sleep(0.1); 

    position = [0,0,0];
    
    while z <= zmax:
        motor3(zspeed,1);
        z += 1;
        while y <= ymax:
                motor1(xspeed,xmax);
                motor2(yspeed,1);
                y += 1;
                motor1(xspeed,-xmax);
                motor2(yspeed,1);
                y += 1;
        

scan(10,20,30,10,10,10,0.001,0.001,0.001);
