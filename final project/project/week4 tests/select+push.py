"""
Program for the sliding mechanism + push test
"""

from utils.brick import Motor, TouchSensor, wait_ready_sensors
from utils.emergency_stop import ES
import time
import cube_selector, push

#Initialize sensors
sensor = TouchSensor(1)
slidemotor = Motor("B")
pushmotor = Motor("C")

POWER_LIMIT = 40       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

wait_ready_sensors(True)
print("Done waiting.")

slidemotor.reset_encoder()                      # Reset encoder to 0 value
slidemotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
slidemotor.set_power(0)

def drop(color):
    """
    Drops the cube of color 'color'
    """
    cube_selector.move_to_cube_position(color)
    time.sleep(1)
    push.push()
    time.sleep(1)
    cube_selector.move_to_base(color)

#Main function
try:
    drop("yellow")
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()
