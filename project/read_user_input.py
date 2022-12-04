#!/usr/bin/env python3


from utils.sound import NOTES, gen_wave
from utils.brick import wait_ready_sensors
import simpleaudio as sa
import time


HOLD_CLICK_DELAY = 0.7

ONE_TOUCH_SENSOR = None
ZERO_TOUCH_SENSOR = None
RESET_TOUCH_SENSOR = None

tone_volume = 100
tone_duration = 0.5

note_map = {
    "append_tone" : "A4",
    "remove_tone" : "B4",
    "error_tone" : "C4",
    "reset_tone" : "G4",
    "complete_tone" : "C5"
}        

def set_touch_sensors(backButton, zeroButton, oneButton):
    global ONE_TOUCH_SENSOR
    global ZERO_TOUCH_SENSOR
    global RESET_TOUCH_SENSOR
    ONE_TOUCH_SENSOR = oneButton
    ZERO_TOUCH_SENSOR = zeroButton
    RESET_TOUCH_SENSOR = backButton

def init_waves():
    # Pre-generate all waves for existing notes
    # Makes the sound playing much faster
    note_waves = {}
    for name, note in note_map.items():
        note_waves[name] = gen_wave(
            tone_duration, 
            tone_volume, 
            NOTES[note], 
            0,0, 0, 0, 1, 0.01, 8000
        )
    return note_waves

def get_touch_input():
    global HOLD_CLICK_DELAY
    if ONE_TOUCH_SENSOR.is_pressed(): #detect click on 0 button
        time_passed = 0
        while RESET_TOUCH_SENSOR.is_pressed():
            time.sleep(0.01)
            time_passed += 0.01
            if time_passed >= HOLD_CLICK_DELAY: return (3, 1)
        return (1, 1)
    elif ZERO_TOUCH_SENSOR.is_pressed(): #detect click on 1 button
        return (0, 1)
    elif RESET_TOUCH_SENSOR.is_pressed(): #detect first click on reset button
        time_passed = 0
        while RESET_TOUCH_SENSOR.is_pressed():
            time.sleep(0.01)
            time_passed += 0.01
            if time_passed >= HOLD_CLICK_DELAY: return (2, 0) #hold click on reset button
        return (2, 1)
    else: return None

def play_sound(player, wave):
    if player is not None and player.is_playing():
        player.stop()
    return sa.play_buffer(wave, 1, 2, 8000) # Returns player

def read_user_input():
    note_waves = init_waves()
    arr = [["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"]]
    print("Single click 1 button to append a '1' to the input array.\n Single click 0 button to append a '0' to the input array. \nSingle click the backspace button to remove the last element from the input array. \nHold click the backspace to submit array, will fill missing entries with 0")
    i = 0
    one_count = 0
    player = None
    while i < 25:
        new_input = get_touch_input()
        if new_input == (3, 1): #submit command
            while arr[4][4] != 0:
                arr[int(i/5)][(i)%5] = 0
                i += 1
            break
        elif new_input == (0, 1):
            arr[int(i/5)][(i)%5] = 0
            i += 1
            print(str(arr))
            player = play_sound(player, note_waves["append_tone"])
        elif new_input == (1, 1):
            if one_count >= 15:
                print("Cannot append another 1. (maximum 15 ones)")
                player = play_sound(player, note_waves["error_tone"])
                continue
            one_count += 1
            arr[int(i/5)][(i)%5] = 1
            i += 1
            print(str(arr))
            player = play_sound(player, note_waves["append_tone"])
        elif new_input == (2, 0):
            arr = [["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"]]
            i = 0
            one_count = 0
            print(str(arr))
            player = play_sound(player, note_waves["reset_tone"])
        elif new_input == (2, 1):
            i -= 1
            if (arr[int(i/5)][(i)%5]) == 1: one_count -= 1
            arr[int(i/5)][(i)%5] = "_"
            print(str(arr))
            player = play_sound(player, note_waves["remove_tone"])
        else: continue
        time.sleep(0.2)

    
    #read in button touches to arr
    player = play_sound(player, note_waves["complete_tone"])
    print("Final array: " + str(arr))
    return arr


if __name__ == "__main__":
    print("Program start. Waiting for sensors.")
    wait_ready_sensors(False) # Input True to see what the robot is trying to initialize! False to be silent.
    print("Done waiting.")

    input_arr = []
    read_user_input(input_arr)

    #once we reach this line our data is valid
                  
    