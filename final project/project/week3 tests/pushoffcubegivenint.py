"""
Program for the sliding mechanism
"""

from utils.brick import Motor, TouchSensor, BP, wait_ready_sensors, EV3ColorSensor 
from utils.emergency_stop import ES
from colors import get_color
import time

#Initialize sensors
stopsensor = TouchSensor(1)
slidemotor = Motor("B")
pushmotor = Motor("C")
zone_color_sensor = EV3ColorSensor(2)

POWER_LIMIT = 40       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

slidemotor.reset_encoder()                      # Reset encoder to 0 value
slidemotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
slidemotor.set_power(0)

wait_ready_sensors(True)
print("Done waiting.")

# amount we need to move to get to next position
step = 98.3

cube_positions = {
    "red": 0,
    "orange": 98.3,
    "yellow": 196.6,
    "green": 294.9,
    "blue": 393.2,
    "purple": 491.5
}

def get_cube_positions():
    return cube_positions

cubes_and_positions = {
    "red": 0, "orange":1, "yellow":2, "green":3, "blue":4, "purple":5
    }

def get_cubes_and_positions():
    return cubes_and_positions

#Move to a specific cube position: works with color name
def move_to_cube_position(color_name):
    position = cube_positions[color_name] 
    slidemotor.set_position_relative(position)
    time.sleep(2)

def move_to_base(current_color):
    position = cube_positions[current_color]
    slidemotor.set_position_relative(-position-1)
    time.sleep(2)
    
def push():
    pushmotor.set_position_relative(360)
    time.sleep(2)
    
def read():
    zone_color = get_color.get_mean_color(zone_color_sensor)
    time.sleep(1)
    last = get_color.get_last_20(zone_color)
    print(last)
    return last

#Main function
try:
    while not stopsensor.is_pressed():
        #Comment out one of those lines depending on what you want to test
        #position = int(input("What position should we move to?"))
        read()

        #same here
        #slidemotor.set_position_relative(382)
        #time.sleep(2)
        #push()
        #slidemotor.set_position_relative(-384)
        
        if zone_color == "red":
            move_to_cube_position("red")
            sleep(2)
            push()
            move_to_base("red")
        
        if zone_color == "orange": 
            move_to_cube_position("orange")
            sleep(2)
            push()
            move_to_base("orange")

        if zone_color == "yellow":  
            move_to_cube_position("yellow")
            sleep(2)
            push()
            move_to_base("yellow")

        if zone_color == "green":
            move_to_cube_position("green")
            sleep(2)
            push()
            move_to_base("green")

        if zone_color == "blue":
            move_to_cube_position("blue")
            sleep(2)
            push()
            move_to_base("blue")

        if zone_color == "purple":
            move_to_cube_position("purple")
            sleep(2)
            push()
            move_to_base("purple")   

    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()

