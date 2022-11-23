
from utils.sound import Sound
from utils.brick import TouchSensor, Motor, wait_ready_sensors, reset_brick
from time import sleep
from read_user_input import set_touch_sensors, read_user_input

class Robot():
    X_DIM = [None, None]
    Y_DIM = [None, None]
    Y2_DIM = [None, None]

    TOLERANCE = 3               # Tolerance (in degrees)
    HOLD_CLICK_DELAY = 0.75     # Time to hold button (in seconds)
    MOTOR_SPEED = 180           # Motors speed (in degrees per second)
    MOTOR_POWER = 100           # Motor power (in %)
    

    def __init__(self):

        self.TOUCH_SENSOR1 = TouchSensor(1) # Left
        self.TOUCH_SENSOR2 = TouchSensor(2) # Right
        self.TOUCH_SENSOR3 = TouchSensor(3) # Reset

        self.MOTOR_X = Motor("C")   # Negative is forward
        self.MOTOR_X.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)
        self.MOTOR_Y1 = Motor("A")  # Positive is forward
        self.MOTOR_Y1.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)
        self.MOTOR_Y2 = Motor("B")  # Negative is forward
        self.MOTOR_Y2.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)

        self.APPEND_TONE = Sound(duration=10, volume=80, pitch="A4")
        self.REMOVE_TONE = Sound(duration=1.0, volume=80, pitch="A4")
        self.RESET_TONE = Sound(duration=1.0, volume=80, pitch="A4")
        self.COMPLETE_TONE = Sound(duration=1.0, volume=80, pitch="A5") 

        wait_ready_sensors(True)

        set_touch_sensors(self.TOUCH_SENSOR3, self.TOUCH_SENSOR2, self.TOUCH_SENSOR1)       # Set initialized sensors in other file as globals

        self.X_INIT_DEG = self.MOTOR_X.get_position()
        self.Y1_INIT_DEG = self.MOTOR_Y1.get_position()
        self.Y2_INIT_DEG = self.MOTOR_Y2.get_position()
    
    def draw_matrix(self, matrix):
        for i in range(len(matrix)-1, -1, -1):
            robot.load_bar_deg(matrix[i])
            robot.push_bar(i)
    
    def calibrate_deg(self):
        DEBUG = 1
        # X calibration first and last position
        for pos in [0, 1]:
            while True:
                if DEBUG: print(self.MOTOR_X.get_position())

                if self.TOUCH_SENSOR1.is_pressed() and self.TOUCH_SENSOR2.is_pressed():
                    if DEBUG: print("BREAKING")
                    sleep(1)
                    break
                elif self.TOUCH_SENSOR1.is_pressed():
                    # Forward
                    self.MOTOR_X.set_position_relative(-10)
                elif self.TOUCH_SENSOR2.is_pressed():
                    # Backward
                    self.MOTOR_X.set_position_relative(10)
                sleep(0.1)
            self.X_DIM[pos] = self.MOTOR_X.get_position()
            if DEBUG: print(f"Dimension {pos}: {self.X_DIM[pos]}")
        self.rotate_motor_deg(self.MOTOR_X, self.X_INIT_DEG)
        
        # Y calibration first and last position
        for pos in [0, 1]:
            while True:
                if DEBUG: print(f"{self.MOTOR_Y1.get_position()}, {self.MOTOR_Y1.get_position()}")

                if self.TOUCH_SENSOR1.is_pressed() and self.TOUCH_SENSOR2.is_pressed():
                    if DEBUG: print("BREAKING")
                    sleep(1)
                    break
                elif self.TOUCH_SENSOR1.is_pressed():
                    # Forward
                    self.MOTOR_Y1.set_position_relative(10)
                    self.MOTOR_Y2.set_position_relative(-10)
                elif self.TOUCH_SENSOR2.is_pressed():
                    # Backward
                    self.MOTOR_Y1.set_position_relative(-10)
                    self.MOTOR_Y2.set_position_relative(10)
                sleep(0.1)
            self.Y_DIM[pos] = self.MOTOR_Y1.get_position()
            self.Y2_DIM[pos] = self.MOTOR_Y2.get_position()
            if DEBUG: print(f"Dimension {pos}: {self.X_DIM[pos]}")
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [self.Y1_INIT_DEG, self.Y2_INIT_DEG])
        with open('dim.csv', 'w') as f:
            f.write(f"{self.X_INIT_DEG}, {self.Y1_INIT_DEG}, {self.Y2_INIT_DEG}\n")
            f.write(f"{self.X_DIM}\n")
            f.write(f"{self.Y_DIM}\n")
            f.write(f"{self.Y2_DIM}\n")
            f.close()

        print(f"Final Dimensions: ({self.X_DIM}) and ({self.Y_DIM}), ({self.Y2_DIM})")
    
    def push_bar(self, idx):
        print("Pushing bar")
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [self.Y1_INIT_DEG, self.Y2_INIT_DEG])
        
        self.rotate_motor_deg(self.MOTOR_X, self.X_INIT_DEG)

        print("Moving cubes")
        inc1 = (self.Y_DIM[0]-self.Y_DIM[1])/4
        inc2 = (self.Y2_DIM[0]-self.Y2_DIM[1])/4
        print("Cube 1")
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [round(self.Y_DIM[0]-inc1*idx), round(self.Y2_DIM[0]-inc2*idx)])
        print("Final pos")
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [self.Y1_INIT_DEG, self.Y2_INIT_DEG])
        print("Next")
        sleep(2)    # Delay for cube to fall

    
    def load_bar_deg(self, arr):
        print("Loading bar")
        self.rotate_motor_deg([self.MOTOR_Y1, self.MOTOR_Y2], [self.Y1_INIT_DEG, self.Y2_INIT_DEG])
        
        self.rotate_motor_deg(self.MOTOR_X, self.X_INIT_DEG)
        
        print("Moving cubes")
        inc = (self.X_DIM[0]-self.X_DIM[1])/4
        for i in range(len(arr)-1, -1, -1):
            if arr[i] == 0: continue
            print("Cube 1")
            self.rotate_motor_deg(self.MOTOR_X, round(self.X_DIM[0]-inc*i))
            print("Final pos")
            self.rotate_motor_deg(self.MOTOR_X, self.X_INIT_DEG)
            print("Next")
            sleep(2)    # Delay for cube to fall
    
    def rotate_motor_deg(self, motors, end_pos):
        if not isinstance(motors, list): motors = [motors]
        if not isinstance(end_pos, list): end_pos = [end_pos]

        print(f"Pos: {end_pos}")
        for i in range(0, len(motors)):
            motors[i].set_position(end_pos[i])    # Move basicall forever
        
        in_position = False
        while True:
            for i in range(0, len(motors)):
                # Break when at least 1 motor is in position
                print(f"Motor{i}: {motors[i].get_position()} degree")
                print(f"Desired: {end_pos[i]} degree")
                cur_pos = motors[i].get_position()
                if abs(cur_pos - end_pos[i]) > self.TOLERANCE:
                    break
                if i == len(motors)-1: in_position = True
            if in_position: break
    
    def get_touch_input(self):
        if self.TOUCH_SENSOR1.is_pressed(): #detect click on 0 button
            return (1, 1)
        elif self.TOUCH_SENSOR2.is_pressed(): #detect click on 1 button
            return (0, 1)
        elif self.TOUCH_SENSOR3.is_pressed(): #detect first click on reset button
            time_passed = 0
            while self.TOUCH_SENSOR3.is_pressed():
                sleep(0.01)
                time_passed += 0.01
                if time_passed >= self.HOLD_CLICK_DELAY: return (2, 0) #hold click on reset button
            return (2, 1)
        else: return None

HEART = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0]
]

if __name__ == "__main__":
    try:
        robot = Robot()
        robot.calibrate_deg()    # move by 8cm
        matrix = []
        read_user_input(matrix)  # Pass by reference
        robot.draw_matrix(matrix)
    except:
        # Handle error feedback here
        pass
    finally:
        reset_brick()
        exit()
