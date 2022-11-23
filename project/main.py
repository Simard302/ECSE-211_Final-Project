
from utils.sound import Sound
from utils.brick import TouchSensor, Motor, wait_ready_sensors, reset_brick
from time import sleep
from json import dump, load
from os import path

DEBUG = 1

class Robot():
    X_DIM = [None, None]        # X Dimensions min, max (in degrees)
    Y1_DIM = [None, None]       # Y1 Dimensions min, max (in degrees)
    Y2_DIM = [None, None]       # Y2 Dimensions min, max (in degrees)

    TOLERANCE = 3               # Tolerance (in degrees)
    HOLD_CLICK_DELAY = 0.75     # Time to hold button (in seconds)
    MOTOR_SPEED = 180           # Motors speed (in degrees per second)
    MOTOR_POWER = 100           # Motor power (in %)

    TONES = {
        "APPEND": "A4",
        "REMOVE": "A4",
        "RESET": "A4",
        "COMPLETE": "A5"
    }
    

    def __init__(self):
        

        self.TOUCH_SENSOR1 = TouchSensor(1)         # Left
        self.TOUCH_SENSOR2 = TouchSensor(2)         # Right
        self.TOUCH_SENSOR3 = TouchSensor(3)         # Reset

        self.MOTOR_X = Motor("C")                   # X motor, Negative is forward
        self.MOTOR_Y1 = Motor("A")                  # Y1 motor, Positive is forward
        self.MOTOR_Y2 = Motor("B")                  # Y2 motor (reverse), Negative is forward

        # Setting limits for all motors
        self.MOTOR_X.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)
        self.MOTOR_Y1.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)
        self.MOTOR_Y2.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)

        # Creating the tones
        self.APPEND_TONE = Sound(duration=10, volume=80, pitch=self.TONES['APPEND'])
        self.REMOVE_TONE = Sound(duration=1.0, volume=80, pitch=self.TONES['REMOVE'])
        self.RESET_TONE = Sound(duration=1.0, volume=80, pitch=self.TONES['RESET'])
        self.COMPLETE_TONE = Sound(duration=1.0, volume=80, pitch=self.TONES['COMPLETE']) 

        # Wait for all sensors to initialize before getting positions
        wait_ready_sensors(True)

        # Get all initial positions of motors (in degrees)
        self.X_INIT_DEG = self.MOTOR_X.get_position()
        self.Y1_INIT_DEG = self.MOTOR_Y1.get_position()
        self.Y2_INIT_DEG = self.MOTOR_Y2.get_position()
    
    def draw_matrix(self, matrix):
        """Calls all necessary functions to place cubes on the grid according to the matrix

        Args:
            matrix (2D, int): 2D array of integers (0 or 1) where 1 is a cube, and 0 is an empty grid slot
        """
        for i in range(len(matrix)-1, -1, -1):
            robot.load_bar_deg(matrix[i])
            robot.push_bar(i)
    
    def calibrate_deg(self, load_existing=True):
        """Calibrates the system to identify the bounds of the grid. Automatically loads parameters if 'calibration.json' exists

        Args:
            load_existing (bool, optional): Load existing calibration parameters (if existing). Defaults to True.
        """
        # Load calibration parameters from JSON
        if load_existing and path.exists('calibration.json'):
            with open('calibration.json', 'r') as f:
                js = load(f)
                self.X_DIM = js['X_DIM'] + self.X_INIT_DEG
                self.Y1_DIM = js['Y1_DIM'] + self.Y1_INIT_DEG
                self.Y2_DIM = js['Y2_DIM'] + self.Y2_INIT_DEG
        
        # X calibration, find min and max positions of the grid
        for pos in [0, 1]:
            while True:
                if DEBUG: print(self.MOTOR_X.get_position())    # Print current position (ONLY IN DEBUG MODE)
                
                # If both buttons are pressed, "lock-in" the current position
                if self.TOUCH_SENSOR1.is_pressed() and self.TOUCH_SENSOR2.is_pressed():
                    if DEBUG: print("BREAKING")                     # Print when "breaking" out of the loop (ONLY IN DEBUG MODE)
                    sleep(1)
                    break
                elif self.TOUCH_SENSOR1.is_pressed():               # Forward
                    self.MOTOR_X.set_position_relative(-10)
                elif self.TOUCH_SENSOR2.is_pressed():               # Backward
                    self.MOTOR_X.set_position_relative(10)
                sleep(0.1)                                          # Sleep (refresh rate)
            self.X_DIM[pos] = self.MOTOR_X.get_position()           # Update current position
            if DEBUG: print(f"Dimension {pos}: {self.X_DIM[pos]}")  # Print final dimensions (ONLY IN DEBUG MODE)
        # Move motor back to its initial position
        self.rotate_motor_deg(self.MOTOR_X, self.X_INIT_DEG)
        
        # Y calibration, find min and max positions of the grid
        for pos in [0, 1]:
            while True:
                if DEBUG: print(f"{self.MOTOR_Y1.get_position()}, {self.MOTOR_Y1.get_position()}")    # Print current position (ONLY IN DEBUG MODE)

                # If both buttons are pressed, "lock-in" the current position
                if self.TOUCH_SENSOR1.is_pressed() and self.TOUCH_SENSOR2.is_pressed():
                    if DEBUG: print("BREAKING")                     # Print when "breaking" out of the loop (ONLY IN DEBUG MODE)
                    sleep(1)
                    break
                elif self.TOUCH_SENSOR1.is_pressed():               # Forward
                    self.MOTOR_Y1.set_position_relative(10)
                    self.MOTOR_Y2.set_position_relative(-10)
                elif self.TOUCH_SENSOR2.is_pressed():               # Backward
                    self.MOTOR_Y1.set_position_relative(-10)
                    self.MOTOR_Y2.set_position_relative(10)
                sleep(0.1)                                          # Sleep (refresh rate)
            self.Y1_DIM[pos] = self.MOTOR_Y1.get_position()         # Update current position
            self.Y2_DIM[pos] = self.MOTOR_Y2.get_position()

            if DEBUG: print(f"Dimension {pos}: ({self.Y1_DIM[pos]}) ({self.Y2_DIM[pos]}")  # Print final dimensions (ONLY IN DEBUG MODE)
        # Move motor back to its initial position
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [self.Y1_INIT_DEG, self.Y2_INIT_DEG])

        # Report final recorded dimensions of the grid
        print(f"Final Dimensions: ({self.X_DIM}) and ({self.Y1_DIM}), ({self.Y2_DIM})")
        with open('calibration.json', 'w') as f:                    # Save calibration to 'calibration.json'
            
            js = {                                                  # Subtract initial position from min and from max position (only save relative position from initial)
                "X_DIM": [x -self.X_INIT_DEG for x in self.X_DIM],              # X Dimensions
                "Y1_DIM": [y1 - self.Y1_INIT_DEG for y1 in self.Y1_DIM],        # Y1 Dimensions
                "Y2_DIM": [y2 - self.Y2_INIT_DEG for y2 in self.Y2_DIM]         # Y2 Dimensions
            }
            dump(js, f)                                             # Dump the dictionary into a json file
    
    def push_bar(self, idx):
        """Push the bar to its desired position (along Y axis)

        Args:
            idx (int): index of the grid line to place the bar (in a 5x5 grid, idx ranges from 0-4)
        """
        
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [self.Y1_INIT_DEG, self.Y2_INIT_DEG])     # Rotate Y motors back to initial position
        self.rotate_motor_deg(self.MOTOR_X, self.X_INIT_DEG)        # Rotate X motor back to initial position

        inc1 = (self.Y1_DIM[0]-self.Y1_DIM[1])/4                    # Calculate the amount of degrees to increment for each gridpoint (Y1)
        inc2 = (self.Y2_DIM[0]-self.Y2_DIM[1])/4                    # Calculate the amount of degrees to increment for each gridpoint (Y2)

        # Rotate both motors until they are in position
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [round(self.Y1_DIM[0]-inc1*idx), round(self.Y2_DIM[0]-inc2*idx)])
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [self.Y1_INIT_DEG, self.Y2_INIT_DEG])     # Rotate Y motors back to initial position
        sleep(2)    # Delay for cube to fall into place

    
    def load_bar_deg(self, arr):
        """Loading the bar with cubes along the X axis

        Args:
            arr (1D, int): array of cube positions (0 or 1) where 1 is a cube
        """
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [self.Y1_INIT_DEG, self.Y2_INIT_DEG])     # Rotate Y motors back to initial position
        self.rotate_motor_deg(self.MOTOR_X, self.X_INIT_DEG)        # Rotate X motor back to initial position
        
        inc = (self.X_DIM[0]-self.X_DIM[1])/4                       # Calculate the amount of degrees to increment for each gridpoint (X)
        for i in range(len(arr)-1, -1, -1):                         # Loop through the array backwards (last to first)
            if arr[i] == 0: continue                                # If there is no cube to place at this position, continue
            self.rotate_motor_deg(self.MOTOR_X, round(self.X_DIM[0]-inc*i))     # Rotate motor to desired position (X)
            self.rotate_motor_deg(self.MOTOR_X, self.X_INIT_DEG)                # Return X motor back to initial position
            sleep(2)    # Delay for cube to fall into place
    
    def rotate_motor_deg(self, motors, end_pos):
        """Rotate the motor(s) to the desired position

        Args:
            motors (MOTOR or [MOTORS]): Motor(s) to move into position (motors in a list will alternate in direction)
            end_pos (int): final desired position of the motor (in degrees)
        """
        if not isinstance(motors, list): motors = [motors]          # If a single motor is supplied (not as a list), turn it into a list of len 1
        if not isinstance(end_pos, list): end_pos = [end_pos]       # If a single end position is supplied (not a list), turn it into a list of len 1

        if DEBUG: print(f"DEBUG - Desired end position: {end_pos}") # Print desired end position (ONLY IN DEBUG MODE)

        for i in range(0, len(motors)):                             # Loop through motors
            motors[i].set_position(end_pos[i])                      # Set position of motors to desired positions
        
        in_position = False
        while not in_position:
            for i in range(0, len(motors)):                         # Loop through motors
                # Break when at least 1 motor is in position
                if DEBUG: print(f"DEBUG - Motor{i}: Current={motors[i].get_position()}, Desired={end_pos[i]}")  # Print current and desired position (ONLY IN DEBUG MODE)
                cur_pos = motors[i].get_position()                  # Update current position
                if abs(cur_pos - end_pos[i]) > self.TOLERANCE:      # if motor is not at the end position (within tolerance), then break
                    break
                if i == len(motors)-1: in_position = True           # Otherwise, if index is at last motor (so all motors are in position), then update in_position
    
    def get_touch_input(self):
        """Read touch input and return the associated code

        Returns:
            Tuple(int, int): Tuple representing the pressed button and the code (button, code)
        """
        if self.TOUCH_SENSOR1.is_pressed():                         # Detect click on 0 button
            return (1, 1)
        elif self.TOUCH_SENSOR2.is_pressed():                       # Detect click on 1 button
            return (0, 1)
        elif self.TOUCH_SENSOR3.is_pressed():                       # Detect first click on reset button
            time_passed = 0
            while self.TOUCH_SENSOR3.is_pressed():
                sleep(0.01)
                time_passed += 0.01
                if time_passed >= self.HOLD_CLICK_DELAY: return (2, 0) # Hold click on reset button
            return (2, 1)                                           # Detect click on reset button
        else: return None
        
    def read_user_input(self):
        """Read the full user input for a 5x5 grid of 0's and 1's

        Returns:
            Array(2d, int): 2D array of 0's and 1's read by the user input
        """
        arr = [["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"]]
        print("Single click 1 button to append a '1' to the input array.\n Single click 0 button to append a '0' to the input array. \n Single click the backspace button to remove the last element from the input array. \n Hold click the backspace button to reset the input array.")
        i = 0
        one_count = 0
        while i < 25:
            new_input = self.get_touch_input()
            if new_input == (0, 1):
                arr[int(i/5)][(i)%5] = 0
                i += 1
                print(str(arr))
                self.APPEND_TONE.play() # Starts append_tone playing
            elif new_input == (1, 1):
                if one_count >= 15:
                    print("Cannot append another 1. (maximum 15 ones)")
                    continue
                one_count += 1
                arr[int(i/5)][(i)%5] = 1
                i += 1
                print(str(arr))
                self.APPEND_TONE.play() # Starts append_tone playing
            elif new_input == (2, 0):
                arr = [["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"], ["_","_","_","_","_"]]
                i = 0
                one_count = 0
                print(str(arr))
                self.RESET_TONE.play() # Starts reset_tone playing
            elif new_input == (2, 1):
                i -= 1
                if (arr[int(i/5)][(i)%5]) == 1: one_count -= 1
                arr[int(i/5)][(i)%5] = "_"
                print(str(arr))
                self.REMOVE_TONE.play() # Starts remove_tone playing
            else: continue
            sleep(0.3)
        #read in button touches to arr
        print("Final array: " + str(arr))
        return arr

# Pre-configured arrays (for fun)
HEART = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0]
]
X = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1]
]

if __name__ == "__main__":
    try:
        robot = Robot()                         # Initialize new Robot
        robot.calibrate_deg()                   # Calibrate robot (auto or manual)
        matrix = robot.read_user_input()        # Read user input array
        robot.draw_matrix(matrix)               # Draw cubes on grid using input array
    except:
        # Handle error feedback here
        pass
    finally:
        # Reset BrickPi on failure
        reset_brick()
        exit()
