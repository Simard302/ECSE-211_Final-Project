from utils.brick import TouchSensor, Motor, wait_ready_sensors, reset_brick
import time
import math



FWD_TOUCH_SENSOR = TouchSensor(1)   
BKWD_TOUCH_SENSOR = TouchSensor(2) 
MOTOR = Motor("A")

refresh_time = 0.05 #seconds
degrees_per_second = 10 #motor speed

#at program start, assume both motors are in fully retracted position

input_arr = [['0','1','0','1','0'], ['1','0','1','0','1'], ['0','1','0','1','0'], ['1','0','1','0','1'], ['0','1','0','1','0']]

if __name__ == "__main__":
    wait_ready_sensors(True)
    self.MOTOR.set_limits(power=50, dps=degrees_per_second)
    print("init value: " + str(MOTOR.get_position()))
    try:
        while True:
            if FWD_TOUCH_SENSOR.is_pressed():
                MOTOR.set_position_relative(5)
                print(MOTOR.get_position())  
            elif BKWD_TOUCH_SENSOR.is_pressed():
                MOTOR.set_position_relative(-5)
                print(MOTOR.get_position())  
            time.sleep(refresh_time)  
    except KeyboardInterrupt:
        print("done.")
        reset_brick()

