#!/usr/bin/env python3


from utils.sound import Sound
from utils.brick import wait_ready_sensors
import time


HOLD_CLICK_DELAY = 0.7

ONE_TOUCH_SENSOR = None
ZERO_TOUCH_SENSOR = None
RESET_TOUCH_SENSOR = None

tone_volume = 100
tone_duration = 0.5

append_tone = Sound(duration=tone_duration, volume=tone_volume, pitch="A4")
remove_tone = Sound(duration=tone_duration, volume=tone_volume, pitch="B4")
error_tone = Sound(duration=tone_duration, volume=tone_volume, pitch="C4")
reset_tone = Sound(duration=tone_duration, volume=tone_volume, pitch="G4")
complete_tone = Sound(duration=tone_duration, volume=tone_volume, pitch="C5")     
        

def set_touch_sensors(backButton, zeroButton, oneButton):
    global ONE_TOUCH_SENSOR
    global ZERO_TOUCH_SENSOR
    global RESET_TOUCH_SENSOR
    ONE_TOUCH_SENSOR = oneButton
    ZERO_TOUCH_SENSOR = zeroButton
    RESET_TOUCH_SENSOR = backButton


def get_touch_input():
    global HOLD_CLICK_DELAY
    if ONE_TOUCH_SENSOR.is_pressed(): #detect click on 0 button
        return (1, 1)
    elif ZERO_TOUCH_SENSOR.is_pressed(): #detect click on 1 button
        return (0, 1)
    elif RESET_TOUCH_SENSOR.is_pressed(): #detect first click on reset button
        time_passed = 0
        while RESET_TOUCH_SENSOR.is_pressed():
            time.sleep(0.01)
            time_passed += 0.01
            if time_passed >= HOLD_CLICK_DELAY: return (3, 1) #hold click on reset button
        return (2, 1)
    else: return None

def read_user_input():
    global complete_tone
    global append_tone
    global remove_tone
    global error_tone
    global reset_tone
    arr = [["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"]]
    print("Single click 1 button to append a '1' to the input array.\n Single click 0 button to append a '0' to the input array. \nSingle click the backspace button to remove the last element from the input array. \nHold click the backspace button to reset the input array.\nPress all three buttons at any time to finalize the input array (any undefined elements will be set to 0).")
    i = 0
    one_count = 0
    while True:
        new_input = get_touch_input()
        if new_input == (3, 1): #submit command
            complete_tone.play()
            print(str(arr))
            return arr
        elif new_input == (0, 1) and i<25:
            arr[int(i/5)][(i)%5] = 0
            i += 1
            print(str(arr))
            append_tone.play() # Starts append_tone playing
            #append_tone.wait_done()
        elif new_input == (1, 1)and i<25:
            if one_count >= 15:
                print("Cannot append another 1. (maximum 15 ones)")
                error_tone.play()
                #error_tone.wait_done()
                continue
            one_count += 1
            arr[int(i/5)][(i)%5] = 1
            i += 1
            print(str(arr))
            append_tone.play() # Starts append_tone playing
            append_tone.wait_done()
        elif new_input == (2, 1):
            i -= 1
            if (arr[int(i/5)][(i)%5]) == 1: one_count -= 1
            arr[int(i/5)][(i)%5] = "_"
            print(str(arr))
            remove_tone.play() # Starts remove_tone playing
            #remove_tone.wait_done()
        else: continue
        time.sleep(0.2)


if __name__ == "__main__":
    print("Program start. Waiting for sensors.")
    wait_ready_sensors(False) # Input True to see what the robot is trying to initialize! False to be silent.
    print("Done waiting.")

    input_arr = []
    read_user_input(input_arr)

    #once we reach this line our data is valid
                  
    