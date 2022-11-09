#!/usr/bin/env python3

"""
This test is used to collect data from the ultrasonic sensor.
It must be run on the robot.
"""

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
import time


DOUBLE_CLICK_DELAY = 0.01  # seconds of delay between measurements

print("Program start. Waiting for sensors.")

TOUCH_SENSOR = TouchSensor(1)


wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")
        
        
def get_touch_input():
    if TOUCH_SENSOR.is_pressed(): #detect first click
        time_passed = 0
        while TOUCH_SENSOR.is_pressed():
            time.sleep(0.01)
            time_passed += 0.01
            if time_passed >= 1: return 0 #hold click
        if time_passed < 1: #check for single or double click
            time_passed = 0
            while not TOUCH_SENSOR.is_pressed():
                time.sleep(0.01)
                time_passed += 0.01
                if time_passed > 0.5: break#check if the button is clicked again within a half second of first click
            #print(time_passed)
            if time_passed > 0.5: return 1 # Single click
            else: return 2 #double click
        else:
            time_passed = 0
            while time_passed < 0.8:
                if not TOUCH_SENSOR.is_pressed():
                    # single click
                    break
                time.sleep(0.01)
                time_passed += 0.01
            if time_passed >= 0.8: return 0 #hold click
            else: return 1 #single click
    else: return None

def read_user_input(arr):
    arr = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
    print("Single click to append a '1' to the input array.\n Double click to append a '0' to the input array. \n Triple click to reset the input array.")
    i = 0
    while i < 25:
        new_input = get_touch_input()
        if new_input == 2:
            arr[int(i/5)][(i)%5] = 0
            i += 1
            print(arr)
            time.sleep(0.5)
        elif new_input == 1:
            arr[int(i/5)][(i)%5] = 1
            print(arr)
            i += 1
            time.sleep(0.5)
        elif new_input == 0:
            arr = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
            print(arr)
            i = 0
            time.sleep(0.5)
        else:
            continue
    #read in button touches to arr
    print(arr)
    
def place_cube(x, y):
    move_arm_up()
    #receives x and y coordinates (0-4, 0-4)
    #find position of robot
    #decide which directions to move motors
    #move motors a small amount in that direction
    #repeat
    #if distance moved is small enough, assume we have reached our destination
    
    move_arm_down()
    release_cube()
    #repeat

if __name__ == "__main__":
    input_arr = []
    valid = False
    while not valid:
        read_user_input(input_arr)
        if len(input_arr) != 5 or len(input_arr[0]) != 5 or input_list.count(1) > 15:
            print("Invalid input. Max. 15 ones. " + str(input_arr))
            continue
        valid = True
                  
    