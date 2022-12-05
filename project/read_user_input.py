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
    "error_tone" : "E5",
    "reset_tone" : "G4",
    "complete_tone" : "Gb5"
}        

def set_touch_sensors(backButton, zeroButton, oneButton):
    """Set touch sensor variables

    Args:
        backButton (TouchSensor): back button sensor
        zeroButton (TouchSensor): zero button sensor
        oneButton (TouchSensor): one button sensor
    """
    global ONE_TOUCH_SENSOR
    global ZERO_TOUCH_SENSOR
    global RESET_TOUCH_SENSOR
    ONE_TOUCH_SENSOR = oneButton
    ZERO_TOUCH_SENSOR = zeroButton
    RESET_TOUCH_SENSOR = backButton

def init_waves():
    """Pre-generate all waves for necessary notes. Makes sound playing much faster

    Returns:
        dict: name:wave dictionary pair
    """
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
    """Convert touch sensor data to input function

    Returns:
        tuple(int, int): code for input function
    """
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

def play_sound(player, wave):
    """Play sound wave. Stop any previous sounds if there were any

    Args:
        player (Player or None): current sound player
        wave (Sound Wave): generated wave to play

    Returns:
        Player: new sound player
    """
    if player is not None and player.is_playing():
        player.stop()
    return sa.play_buffer(wave, 1, 2, 8000) # Returns player

def convert_char(x):
    """Converts the array char to the char to print

    Args:
        x (int or str): character to convert

    Returns:
        char: converted character
    """
    if x==0: return ' '
    elif x == 1: return 'X'
    else: return x

def read_user_input():
    """Read user input and generate a matrix for the mosaic

    Returns:
        2D array: matrix for the mosaic
    """
    note_waves = init_waves()
    arr = [["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"]]
    print("Single click 1 button to append a '1' to the input array.\nSingle click 0 button to append a '0' to the input array. \nSingle click the backspace button to remove the last element from the input array. \nHold click the backspace to submit array, will fill missing entries with 0")
    i = 0
    one_count = 0
    player = None
    while True:
        new_input = get_touch_input()
        if new_input == (3, 1): #submit command
            while arr[4][4] != 0 and arr[4][4] != 1:
                arr[int(i/5)][(i)%5] = 0
                i += 1
            player = play_sound(player, note_waves["complete_tone"])
            print("Final Mosaic: ")
            print("=========")
            [print(*(convert_char(x) for x in reversed(row)), sep=' ') for row in arr]
            time.sleep(2)
            return arr
        elif new_input == (0, 1):
            if i>=25:
                print("Cannot append another 0. (full array)")
                player = play_sound(player, note_waves["error_tone"])
                time.sleep(0.2)
                continue
            arr[int(i/5)][(i)%5] = 0
            i += 1
            print("=========")
            [print(*(convert_char(x) for x in reversed(row)), sep=' ') for row in arr]
            player = play_sound(player, note_waves["append_tone"])
        elif new_input == (1, 1):
            if i>=25:
                print("Cannot append another 1. (full array)")
                player = play_sound(player, note_waves["error_tone"])
                time.sleep(0.2)
                continue
            if one_count >= 15:
                print("Cannot append another 1. (maximum 15 ones)")
                player = play_sound(player, note_waves["error_tone"])
                time.sleep(0.2)
                continue
            one_count += 1
            arr[int(i/5)][(i)%5] = 1
            i += 1
            print("=========")
            [print(*(convert_char(x) for x in reversed(row)), sep=' ') for row in arr]
            player = play_sound(player, note_waves["append_tone"])
        elif new_input == (2, 1):
            i -= 1
            if (arr[int(i/5)][(i)%5]) == 1: one_count -= 1
            arr[int(i/5)][(i)%5] = "_"
            print("=========")
            [print(*(convert_char(x) for x in reversed(row)), sep=' ') for row in arr]
            player = play_sound(player, note_waves["remove_tone"])
        else:continue
        time.sleep(0.2)
                  
    