
from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, EV3ColorSensor, wait_ready_sensors, reset_brick
from time import sleep
from math import exp

class Robot():
    CM_PER_360 = 13.823 # 4.4cm diamete*pi
    FLEX_STATE = 0

    TOLERANCE_X = 0.1
    

    def __init__(self):
        self.US_SENSOR_X = EV3UltrasonicSensor(1)
        self.US_SENSOR_Y = EV3UltrasonicSensor(2)

        self.TOUCH_SENSOR = TouchSensor(3)
        self.COLOR_SENSOR = EV3ColorSensor(4)

        wait_ready_sensors(True)

        self.X_INIT = self.US_SENSOR_X.get_value()
        self.Y_INIT = self.US_SENSOR_Y.get_value()
        self.X_POS = 0
        self.Y_POS = 0
    

    def update_gridpoint(self):
        # distance*(1-e^(-x))
        
        x_cm = self.US_SENSOR_X.get_value() - self.xinit
        y_cm = self.US_SENSOR_Y.get_value() - self.yinit

        self.X_POS = round(x_cm / 20) -1  # Convert cm reading to gridpoint
        self.Y_POS = round(y_cm / 20) -1  # Convert cm reading to gridpoint

        return self.X_POS, self.Y_POS
    
    def move_to_gridpoint(self, x, y):
        pass

    def rotate_motor(self, grid_x, grid_y):
        end_x = self.X_INIT + 4*(grid_x+1)
        end_y = self.Y_INIT + 4*(grid_y+1)
        start_x = self.US_SENSOR_X.get_value() - self.X_INIT
        start_y = self.US_SENSOR_Y.get_value() - self.Y_INIT

        total_degrees = (end_x - start_x) * 360 / self.CM_PER_360


        while True:
            cur_x = self.US_SENSOR_X.get_value() - self.X_INIT
            if end_x - cur_x > self.TOLERANCE_X:
                total_degrees*exp(-(cur_x - start_x))
                self.MOTOR_X.set_position_relative(total_degrees*exp(-(cur_x - start_x))))
            


if __name__ == "__main__":
    try:
        robot = Robot()
        robot.run()
    except:
        # Handle error feedback here
        pass
    finally:
        reset_brick()
        exit()
