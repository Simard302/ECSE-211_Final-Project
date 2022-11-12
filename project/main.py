
from utils.brick import TouchSensor, EV3UltrasonicSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
from time import sleep
from math import exp

class Robot():
    CM_PER_360 = 13.823 # 4.4cm diamete*pi
    FLEX_STATE = 0

    TOLERANCE = 0.1
    MOTOR_SPEED = 60
    MOTOR_POWER = 100
    

    def __init__(self):
        self.US_SENSOR_X = EV3UltrasonicSensor(1)
        #self.US_SENSOR_Y = EV3UltrasonicSensor(2)

        #self.TOUCH_SENSOR = TouchSensor(3)
        #self.COLOR_SENSOR = EV3ColorSensor(4)

        self.MOTOR_X = Motor("A")
        self.MOTOR_X.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)
        #self.MOTOR_Y = Motor("B")
        #self.MOTOR_Y.set_limits(power=self.MOTOR_POWER, dps=self.MOTOR_SPEED)

        wait_ready_sensors(True)

        self.X_INIT = self.US_SENSOR_X.get_value()
        #self.Y_INIT = self.US_SENSOR_Y.get_value()
        self.X_POS = 0
        self.Y_POS = 0
    

    def update_gridpoint(self):
        # distance*(1-e^(-x))
        
        x_cm = self.US_SENSOR_X.get_value() - self.X_INIT
        #y_cm = self.US_SENSOR_Y.get_value() - self.Y_INIT

        self.X_POS = round(x_cm / 20) -1  # Convert cm reading to gridpoint
        #self.Y_POS = round(y_cm / 20) -1  # Convert cm reading to gridpoint

        #return self.X_POS, self.Y_POS
    
    def move_to_gridpoint(self, x, y):
        pass

    def rotate_motor(self, grid_x, grid_y):
        # All positions in cm
        print(f"I am here {self.X_INIT}cm")
        end_x = self.X_INIT - 4*(grid_x)
        if end_x < 0: end_x = 0
        #end_y = self.Y_INIT + 4*(grid_y)

        t = 0.5
        self.MOTOR_X.set_position_relative((end_x - 0)*(360/self.CM_PER_360))
        while True:
            cur_x = self.US_SENSOR_X.get_value()
            print(f"Distance left: {abs(end_x - cur_x)}")
            if abs(end_x - cur_x) > self.TOLERANCE:
                # Calc degree velocity
                deg_vel = (1-exp(-abs(end_x-cur_x)))*10 * (360 / self.CM_PER_360)  # 2 is hyperparameter
                self.MOTOR_X.set_dps(deg_vel)   # Set motor velocity to dps
                
                sleep(0.25) # Wait for motor to stop spinning(0.25s) + buffer(0.5s)
                t += 0.25
            else:
                break
        
        """t = 0.5
        self.MOTOR_Y.set_position_relative((end_y - 0)*(360/self.CM_PER_360))
        while True:
            cur_y = self.US_SENSOR_Y.get_value()
            print(f"Distance left: {abs(end_y - cur_y)}")
            if abs(end_y - cur_y) > self.TOLERANCE:
                # Calc degree velocity
                deg_vel = (1-exp(-abs(end_y-cur_y)))*10 * (360 / self.CM_PER_360)  # 2 is hyperparameter
                self.MOTOR_Y.set_dps(deg_vel)   # Set motor velocity to dps
                
                sleep(0.25) # Wait for motor to stop spinning(0.25s) + buffer(0.5s)
                t += 0.25
            else:
                break"""
        


if __name__ == "__main__":
    try:
        robot = Robot()
        robot.rotate_motor(5, 0)    # move by 8cm
    except:
        # Handle error feedback here
        pass
    finally:
        reset_brick()
        exit()
