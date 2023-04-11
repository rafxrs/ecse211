""""
Fourth version of software
Code to push cube off using piston
This code works perfectly
We need a set_position_relative of 360 degrees for a full piston rotation (for one push)
"""

from utils.brick import BP, TouchSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
import time

sensor = TouchSensor(1)
pushmotor = Motor("C")

#This is a testing file to test a single motor

PUSH_POWER_LIMIT = 40       # Power limit (percentage)
PUSH_SPEED_LIMIT = 360      # Speed limit in degree per second

wait_ready_sensors(True)
print("Done waiting.")

pushmotor.reset_encoder()                      # Reset encoder to 0 value
pushmotor.set_limits(PUSH_POWER_LIMIT, PUSH_SPEED_LIMIT) # Set the power and speed limits
pushmotor.set_power(0)

def push():
    """
    Activates the piston 
    """
    pushmotor.set_position_relative(360)
    time.sleep(3)

time.sleep(2)
try:

    #Test the piston
    while not sensor.is_pressed():
        push()
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()