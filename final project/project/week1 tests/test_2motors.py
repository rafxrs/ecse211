""" 
A simple test program that tests the two wheel motors at the same time
We can change the set power values anytime to test to turn left or right, etc...
"""
from utils.brick import BP, TouchSensor, Motor, wait_ready_sensors
import time
from utils.emergency_stop import ES

leftmotor = Motor("A")
rightmotor = Motor("B")
sensor = TouchSensor(1)

wait_ready_sensors(True)
print("Done waiting.")

try:
    while not sensor.is_pressed():
        leftmotor.set_power(40)
        rightmotor.set_power(40)
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()



