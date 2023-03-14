"""
Script to follow the path and stop + adjust when we see green
This code is not yet working, we just created the file
"""

from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
from collections import deque
from colors import get_color
import time, math


leftmotor = Motor("D")
rightmotor = Motor("A")
cranemotor = Motor("B")
color_sensor = EV3ColorSensor(3)
sensor = TouchSensor(1)
actionsensor = TouchSensor(4)

wait_ready_sensors(True)
print("Done waiting.")

#This is for the crane
POWER_LIMIT = 20       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]
    
def adjust_robot():
    """
    Function that puts the robot exactly on the green line when we see green 
    """


def crane():
    cranemotor.reset_encoder()                      # Reset encoder to 0 value
    cranemotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits

delivery_colors= []
def follow_path():
    """
    Function that follows the path: if we see red we turn left, blue we turn right, else 
    we keep going
    """
    try:
        path= get_color.get_mean_color(color_sensor)
        
        if path in mapred:
            leftmotor.set_power(35)
            rightmotor.set_power(8)
        elif path in mapblue: 
            leftmotor.set_power(35)
            rightmotor.set_power(8)
        else:
            leftmotor.set_power(18)
            rightmotor.set_power(18)
    
    except BaseException as error:
        print(error)

def follow_path_and_adjust():
    follow_path()


# Main function
time.sleep(4)
try:
    while not sensor.is_pressed():
        follow_path()
    print(delivery_colors)
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()