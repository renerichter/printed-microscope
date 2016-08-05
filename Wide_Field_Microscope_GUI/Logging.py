# -*- coding: utf-8 -*-
"""
Created on Sat May 28 12:15:53 2016

@author: pi
"""

"""
This is a short file testing the concept of a log file
to keep track of the position of the stepper motors
in the 3D printed microscope
"""

import sys
position=[1,2,3]

while True:

    direction = input("New direction for change (x,y,z) or show current position (p): ")
        
    if direction == 'x':
        new_value = int(input("New value: "))
        position[0] = new_value
    elif direction == 'y':
        new_value = int(input("New value: "))
        position[1] = new_value
    elif direction == 'z':
        new_value = int(input("New value: "))
        position[2] = new_value
    elif direction == 'p':
        print (position)
    elif direction == 'exit':
        break
        

#for i in range(1,4):
#    
#   # print (os.getcwd())     
#    
#    f = open('logtest.txt', 'r')
##    logtest = f.readlines()
##    print (logtest)
#    
#   # logtest = f.readlines()
#    print (i)    
#    position[i-1] = f
#    
#    f.close()    
#    

