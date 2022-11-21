
from utils.brick import TouchSensor, EV3UltrasonicSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
from time import sleep
from math import exp

class Robot():
    X_DIM = [None, None]
    Y_DIM = [None, None]
    Y2_DIM = [None, None]
    CM_PER_360 = 13.823 # 4.4cm diamete*pi

    TOLERANCE = 0.5
    DOUBLE_CLICK_DELAY = 0.5
    HOLD_CLICK_DELAY = 1
    MOTOR_SPEED = 180
    MOTOR_POWER = 100
    

    def __init__(self):
        self.US_SENSOR_X = EV3UltrasonicSensor(1)
        self.US_SENSOR_Y = EV3UltrasonicSensor(3)

        self.TOUCH_SENSOR1 = TouchSensor(2) # Left
        self.TOUCH_SENSOR2 = TouchSensor(4) # Right

        self.MOTOR_X = Motor("C")   # Negative is forward
        self.MOTOR_X.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)
        self.MOTOR_Y1 = Motor("A")  # Positive is forward
        self.MOTOR_Y1.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)
        self.MOTOR_Y2 = Motor("B")  # Negative is forward
        self.MOTOR_Y2.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)

        wait_ready_sensors(True)

        self.X_INIT_US = self.US_SENSOR_X.get_value()
        self.X_INIT_DEG = self.MOTOR_X.get_position()
        print(f"Initial X: {self.X_INIT_US}")
        self.Y_INIT_US = self.US_SENSOR_Y.get_value()
        self.Y1_INIT_DEG = self.MOTOR_Y1.get_position()
        self.Y2_INIT_DEG = self.MOTOR_Y2.get_position()
        print(f"Initial Y: {self.Y_INIT_US}")
    
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

    @DeprecationWarning
    def calibrate_us(self):
        DEBUG = 1
        # X calibration first and last position
        for pos in [0, 1]:
            if self.X_DIM[pos] is not None: continue
            while True:
                if DEBUG: print(self.US_SENSOR_X.get_value())

                if self.TOUCH_SENSOR1.is_pressed() and self.TOUCH_SENSOR2.is_pressed():
                    if DEBUG: print("BREAKING")
                    sleep(1)
                    break
                elif self.TOUCH_SENSOR1.is_pressed():
                    # Forward
                    self.MOTOR_X.set_position_relative(-5)
                elif self.TOUCH_SENSOR2.is_pressed():
                    # Backward
                    self.MOTOR_X.set_position_relative(5)
                sleep(0.05)
            self.X_DIM[pos] = self.US_SENSOR_X.get_value()
            if DEBUG: print(f"Dimension {pos}: {self.X_DIM[pos]}")
        self.rotate_motor_us(self.MOTOR_X, self.US_SENSOR_X, self.X_INIT_US, 1)
        
        # Y calibration first and last position
        for pos in [0, 1]:
            if self.Y_DIM[pos] is not None and self.Y2_DIM[pos] is not None: continue
            while True:
                if DEBUG: print(self.US_SENSOR_X.get_value())

                if self.TOUCH_SENSOR1.is_pressed() and self.TOUCH_SENSOR2.is_pressed():
                    if DEBUG: print("BREAKING")
                    sleep(1)
                    break
                elif self.TOUCH_SENSOR1.is_pressed():
                    # Forward
                    self.MOTOR_Y1.set_position_relative(5)
                    self.MOTOR_Y2.set_position_relative(-5)
                elif self.TOUCH_SENSOR2.is_pressed():
                    # Backward
                    self.MOTOR_Y1.set_position_relative(-5)
                    self.MOTOR_Y2.set_position_relative(5)
                sleep(0.05)
            self.Y_DIM[pos] = self.US_SENSOR_Y.get_value()
            if DEBUG: print(f"Dimension {pos}: {self.X_DIM[pos]}")
        self.rotate_motor_us([self.MOTOR_Y1, self.MOTOR_Y2], self.US_SENSOR_Y, self.Y_INIT_US, -1)

        print(f"Final Dimensions: ({self.X_DIM}) and ({self.Y_DIM})")
    
    def eq(self, pos1, pos2):
        return abs(pos1-pos2) < self.TOLERANCE
    
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
    
    @DeprecationWarning
    def load_bar_us(self, arr):
        print("Loading bar")
        if not self.eq(self.US_SENSOR_Y.get_value(), self.Y_INIT_US):
            # Add extra 2cm to make sure the pusher is at the end
            print("Resetting Y")
            self.rotate_motor_us([self.MOTOR_Y1, self.MOTOR_Y2], self.US_SENSOR_Y, self.Y_INIT_US, -1)
        
        pos = self.US_SENSOR_X.get_value()
        if not self.eq(pos, self.X_INIT_US):
            print("Resetting X")
            self.rotate_motor_us(self.MOTOR_X, self.US_SENSOR_X, self.X_INIT_US, 1)
        
        print("Moving cubes")
        inc = (self.X_DIM[0]-self.X_DIM[1])/(len(arr)-1)
        for i in range(len(arr)-1, -1, -1):
            if arr[i] == 0: continue
            print("Cube 1")
            self.rotate_motor_us(self.MOTOR_X, self.US_SENSOR_X, self.X_DIM[0]-inc*i, -1)
            print("Final pos")
            self.rotate_motor_us(self.MOTOR_X, self.US_SENSOR_X, self.X_INIT_US, 1)
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
                if abs(cur_pos - end_pos[i])>3:
                    break
                if i == len(motors)-1: in_position = True
            if in_position: break
                
    @DeprecationWarning
    def rotate_motor_us(self, motors, sensor, end_pos, dir):
        if not isinstance(motors, list): motors = [motors]
        
        t = 0.5
        for i in range(0, len(motors)):
            print(f"Pos{i}: {dir*9999*pow(-1, i)}")
            motors[i].set_position_relative(dir*9999*pow(-1, i))    # Move basicall forever
        while True:
            cur = sensor.get_value()
            print(f"Distance left: {abs(end_pos - cur)}")
            print(f"Desired pos: {end_pos}")
            if not self.eq(end_pos, cur):
                # Calc degree velocity
                #k = 10  # hyperparameter
                #deg_vel = (1-exp(-abs(end_pos-cur)))*k * (360 / self.CM_PER_360)
                #print(deg_vel)
                #for i in range(0, len(motors)):
                    #motor[i].set_dps(deg_vel*pow(-1, i))   # Set motor velocity to dps
                
                sleep(0.25) # Wait for motor to stop spinning(0.25s) + buffer(0.5s)
                t += 0.25
            else:
                # stop motors
                for motor in motors:
                    motor.set_position_relative(0)
                break
    
    def get_touch_input(self, TOUCH_SENSOR):
        if TOUCH_SENSOR.is_pressed(): #detect first click
            duration_of_first_click = 0
            while TOUCH_SENSOR.is_pressed(): #in this while loop we record how long the first click is held
                sleep(0.01)
                duration_of_first_click += 0.01
                if duration_of_first_click >= self.HOLD_CLICK_DELAY: return 0 #hold click if first click is held long enough
            #if we're here it's not a hold click, and the first click was released
            time_between_clicks = 0
            while not TOUCH_SENSOR.is_pressed(): #this while loop records the delay after the first click
                sleep(0.01)
                time_between_clicks += 0.01
                if time_between_clicks > self.DOUBLE_CLICK_DELAY: return 1 #if the delay is long enough then it is a single click
            #if we reach this line, the user clicked the button again within the double click delay
            return 2 #double click
        else: return None #if there is no initial click we do nothing
        
    def read_user_input(self):
        arr = [['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_']]
        print("Left click to append a '1' to the input array.")
        print("Right click to append a '0' to the input array.")
        print("Double click either to remove last digit from array.")
        print("Hold either to reset the array.")
        i = 0
    one_count = 0
    while i < 25:
        left_input = get_touch_input() #detect type of click 
        right_input = get_touch_input()
        if left_input == 0 or right_input == 0:
            arr = [['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_']]
            print("Reset input to: " + str(arr))
            i = 0
            one_count = 0
            sleep(0.5)
        elif left_input == 2 or right_input == 2:
            i -= 1
            digit = arr[int(i/4)][(i)%5]
            arr[int(i/4)][(i)%5] = '_'
            if digit == 1: one_count -= 1
            print(f"Removed {digit}: {arr}")
            sleep(0.5)
        if new_input == 2: #double click
            if one_count >= 15:
                print("Warning: Cannot append another 1. (maximum 15 ones per input)")
                continue
            arr[int(i/5)][(i)%5] = 1
            i += 1
            one_count += 1
            print("Appended 1: " + str(arr))
            sleep(0.5)
        elif new_input == 1: #single click
            arr[int(i/5)][(i)%5] = 0
            print("Appended 0: " + str(arr))
            i += 1
            sleep(0.5)
        elif new_input == 0: #hold
            arr = [['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_'], ['_','_','_','_','_']]
            print("Reset input to: " + str(arr))
            i = 0
            one_count = 0
            sleep(0.5)
    return arr



if __name__ == "__main__":
    try:
        robot = Robot()
        #robot.X_DIM = [276, -178]
        #robot.Y_DIM = [-151, 304]
        #robot.Y2_DIM = [-117, -570]
        robot.calibrate_deg()    # move by 8cm
        matrix = [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0]
        ]
        for i in range(len(matrix)-1, -1, -1):
            robot.load_bar_deg(matrix[i])
            robot.push_bar(i)
    except:
        # Handle error feedback here
        pass
    finally:
        reset_brick()
        exit()
