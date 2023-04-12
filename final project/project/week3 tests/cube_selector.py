"""
Fourth version of software
Program for the sliding mechanism
"""

from utils.brick import Motor, TouchSensor, BP, wait_ready_sensors
from utils.emergency_stop import ES
import time

#Initialize sensors
stopsensor = TouchSensor(1)
slidemotor = Motor("B")

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

#Move to a specific cube position: works with color name
def move_to_cube_position(color_name):
    position = cube_positions[color_name] 
    slidemotor.set_position_relative(position)
    time.sleep(2)

# Moves back to the initial position from a certain position (color)
def move_to_base(current_color):
    position = cube_positions[current_color]
    slidemotor.set_position_relative(-position-1)
    time.sleep(2)

#Main function
try:
    # Comment out as needed for testing

    # move_to_cube_position("red")
    # move_to_base("red")
        

    # move_to_cube_position("orange")
    # move_to_base("orange")

    # move_to_cube_position("yellow")
    # move_to_base("yellow")

    # move_to_cube_position("green")
    # move_to_base("green")

    # move_to_cube_position("blue")
    # move_to_base("blue")

    # move_to_cube_position("purple")
    # move_to_base("purple")     

    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()
