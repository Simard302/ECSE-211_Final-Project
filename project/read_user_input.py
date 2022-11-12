#!/usr/bin/env python3

"""
This test is used to collect data from the ultrasonic sensor.
It must be run on the robot.
"""

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
import time
import pickle

DOUBLE_CLICK_DELAY = 0.5  # seconds of delay between measurements
HOLD_CLICK_DELAY = 1
TOUCH_SENSOR = TouchSensor(1)       
        
def get_touch_input():
    if TOUCH_SENSOR.is_pressed(): #detect first click
        duration_of_first_click = 0
        while TOUCH_SENSOR.is_pressed(): #in this while loop we record how long the first click is held
            time.sleep(0.01)
            duration_of_first_click += 0.01
            if duration_of_first_click >= HOLD_CLICK_DELAY: return 0 #hold click if first click is held long enough
        #if we're here it's not a hold click, and the first click was released
        time_between_clicks = 0
        while not TOUCH_SENSOR.is_pressed(): #this while loop records the delay after the first click
            time.sleep(0.01)
            time_between_clicks += 0.01
            if time_between_clicks > DOUBLE_CLICK_DELAY: return 1 #if the delay is long enough then it is a single click
        #if we reach this line, the user clicked the button again within the double click delay
        return 2 #double click
    else: return None #if there is no initial click we do nothing

def read_user_input(arr):
    arr = [['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_']]
    print("Single click to append a '0' to the input array.")
    print("Double click to append a '1' to the input array.")
    print("Hold click to reset the array.")
    i = 0
    one_count = 0
    while i < 25:
        new_input = get_touch_input() #detect type of click 
        if new_input == 2: #double click
            if one_count >= 15: print("Warning: Cannot append another 1. (maximum 15 ones per input)")
            arr[int(i/5)][(i)%5] = 1
            i += 1
            one_count += 1
            print("Appended 1: " + str(arr))
            time.sleep(0.5)
        elif new_input == 1: #single click
            arr[int(i/5)][(i)%5] = 0
            print("Appended 0: " + str(arr))
            i += 1
            time.sleep(0.5)
        elif new_input == 0: #hold
            arr = [['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_']]
            print("Reset input to: " + str(arr))
            i = 0
            one_count = 0
            time.sleep(0.5)

if __name__ == "__main__":
    print("Program start. Waiting for sensors.")
    wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
    print("Done.")
    input_arr = read_user_input() #reads the user's input into input_arr until a valid array is obtained

    #once we reach this line our data is valid and can be used

    