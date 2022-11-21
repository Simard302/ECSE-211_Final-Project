#!/usr/bin/env python3

"""
This test is used to collect data from the ultrasonic sensor.
It must be run on the robot.
"""

from utils.sound import Sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
import time


HOLD_CLICK_DELAY = 1

print("Program start. Waiting for sensors.")

ONE_TOUCH_SENSOR = TouchSensor(1)
ZERO_TOUCH_SENSOR = TouchSensor(2)
RESET_TOUCH_SENSOR = TouchSensor(3)


append_tone = Sound(duration=1.0, volume=80, pitch="G4")
remove_tone = Sound(duration=2.0, volume=80, pitch="A4")
reset_tone = Sound(duration=2.0, volume=80, pitch="B4")
complete_tone = Sound(duration=0.5, volume=80, pitch="C5")


wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")
        
        
def get_touch_input():
    if ONE_TOUCH_SENSOR.is_pressed(): #detect click on 0 button
        return (0, 1)
    elif ZERO_TOUCH_SENSOR.is_pressed(): #detect click on 0 button
        return (1, 1)
    elif RESET_TOUCH_SENSOR.is_pressed(): #detect first click on reset button
        time_passed = 0
        while RESET_TOUCH_SENSOR.is_pressed():
            time.sleep(0.01)
            time_passed += 0.01
            if time_passed >= HOLD_CLICK_DELAY: return (2, 0) #hold click on reset button
        return (2, 1)
    else: return None

def read_user_input(arr):
    arr = [["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"]]
    print("Single click 1 button to append a '1' to the input array.\n Single click 0 button to append a '0' to the input array. \n Single click the backspace button to remove the last element from the input array. \n Hold click the backspace button to reset the input array.")
    i = 0
    while i < 25:
        new_input = get_touch_input()
        if new_input == (0, 1):
            arr[int(i/5)][(i)%5] = 0
            i += 1
            print(arr)
            append_tone.play() # Starts append_tone playing
            append_tone.wait_done() # Will wait until append_tone is done playing (0.5 seconds)
        elif new_input == (1, 1):
            arr[int(i/5)][(i)%5] = 1
            i += 1
            print(arr)
            append_tone.play() # Starts append_tone playing
            append_tone.wait_done() # Will wait until append_tone is done playing (0.5 seconds)
        elif new_input == (2, 0):
            arr = [["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"]]
            print(arr)
            i = 0
            reset_tone.play() # Starts reset_tone playing
            reset_tone.wait_done() # Will wait until reset_tone is done playing (0.5 seconds)
        elif new_input == (2, 1):
            i -= 1
            arr[int(i/5)][(i)%5] = "_"
            print(arr)
            remove_tone.play() # Starts remove_tone playing
            remove_tone.wait_done() # Will wait until remove_tone is done playing (0.5 seconds)
        else:
            continue
    #read in button touches to arr
    print("Final array: " + str(arr))


if __name__ == "__main__":
    input_arr = []
    read_user_input(input_arr)

    #once we reach this line our data is valid
                  
    