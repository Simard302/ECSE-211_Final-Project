
from utils.brick import TouchSensor, EV3UltrasonicSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
from time import sleep
from math import exp

class Robot():
    X_DIM = [None, None]
    Y_DIM = [None, None]
    CM_PER_360 = 13.823 # 4.4cm diamete*pi

    TOLERANCE = 0.5
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

        self.X_INIT = self.US_SENSOR_X.get_value()
        print(f"Initial X: {self.X_INIT}")
        self.Y_INIT = self.US_SENSOR_Y.get_value()
        print(f"Initial Y: {self.Y_INIT}")

    def calibrate(self):
        DEBUG = 1
        # X calibration first and last position
        for pos in [0, 1]:
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
        self.rotate_motor(self.MOTOR_X, self.US_SENSOR_X, self.X_INIT, 1)
        
        # Y calibration first and last position
        for pos in [0, 1]:
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
        self.rotate_motor([self.MOTOR_Y1, self.MOTOR_Y2], self.US_SENSOR_Y, self.Y_INIT, -1)

        print(f"Final Dimensions: ({self.X_DIM}) and ({self.Y_DIM})")
    
    def eq(self, pos1, pos2):
        return abs(pos1-pos2) < self.TOLERANCE
        
    def load_bar(self, arr):
        print("Loading bar")
        if not self.eq(self.US_SENSOR_Y.get_value(), self.Y_INIT):
            # Add extra 2cm to make sure the pusher is at the end
            print("Resetting Y")
            self.rotate_motor([self.MOTOR_Y1, self.MOTOR_Y2], self.US_SENSOR_Y, self.Y_INIT, -1)
        
        pos = self.US_SENSOR_X.get_value()
        if not self.eq(pos, self.X_INIT):
            print("Resetting X")
            self.rotate_motor(self.MOTOR_X, self.US_SENSOR_X, self.X_INIT, 1)
        
        print("Moving cubes")
        inc = (self.X_DIM[0]-self.X_DIM[1])/(len(arr)-1)
        for i in range(len(arr)-1, -1, -1):
            if arr[i] == 0: continue
            print("Cube 1")
            self.rotate_motor(self.MOTOR_X, self.US_SENSOR_X, self.X_DIM[0]-inc*i, -1)
            print("Final pos")
            self.rotate_motor(self.MOTOR_X, self.US_SENSOR_X, self.X_INIT, 1)
            print("Next")
            sleep(2)    # Delay for cube to fall

    def rotate_motor(self, motors, sensor, end_pos, dir):
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
        


if __name__ == "__main__":
    try:
        robot = Robot()
        robot.calibrate()    # move by 8cm
        robot.load_bar([1, 1, 0, 1, 0])
    except:
        # Handle error feedback here
        pass
    finally:
        reset_brick()
        exit()
