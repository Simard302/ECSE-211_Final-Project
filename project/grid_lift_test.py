from utils.brick import Motor
import time
grid_lifter = Motor("C")

#set motor limit
grid_lifter.set_limits(power=50, dps=90)

#rotate grid lift motor 25 times
for i in range(24):
    grid_lifter.set_position_relative(-5)
    time.sleep(0.5)
    grid_lifter.set_position_relative(5)
    time.sleep(1)