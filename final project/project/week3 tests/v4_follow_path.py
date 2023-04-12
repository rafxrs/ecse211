"""""
Fourth version of software
In this version, we use two color sensors, one far ahead of the robot to follow the path accurately
The second color sensor is static and on top of the delivery zone and its role is to detect the delivery color
If the green line is detected, the goal is to keep driving unitl we have the wheels on the green zone (or until the second color sensor reads a delivery zone value)
This is all done in this file
"""

from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
import time
from colors import get_color
import cube_selector

leftmotor = Motor("D")
rightmotor = Motor("A")
pushmotor= Motor("C")
slidemotor = Motor("B")
front_color_sensor = EV3ColorSensor(3)
zone_color_sensor = EV3ColorSensor(2)
sensor = TouchSensor(1)

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]
cubes_and_positions = {
    "red": 0, "orange":1, "yellow":2, "green":3, "blue":4, "purple":5
    }

wait_ready_sensors(True)
print("Done waiting.")

POWER_LIMIT = 40       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

def read():
    """
    Function to read the delivery zone color
    This returns the mean of the last 20 mean values the zone color sensor was reading
    """
    zone_color = get_color.get_mean_back_color(zone_color_sensor)
    time.sleep(1)
    last = get_color.get_last_20(zone_color)
    print(last)
    return last

def push():
    """
    Function that pushes the cube that is currently in front of the piston
    """
    pushmotor.reset_encoder()                      # Reset encoder to 0 value
    pushmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    pushmotor.set_power(0)

    #Test the piston
    pushmotor.set_position_relative(360)
    time.sleep(3)

def drop(color):
    """
    Drops the cube of color 'color'
    First, we slide to get the right position
    Then, we push
    """
    cube_selector.move_to_cube_position(color)
    push()
    

def follow_path():
    """
    The iconic follow path function
    Here, we follow the path, and when our zone color sensor stops seeing white, which means we reached a delivery zone,
    we get the color that the zone color sensor is seeing, slide the cube of that colour in the dropoff position, and push it
    
    """
    try:
        delivery_colors = []
        front_color= get_color.get_mean_front_color(front_color_sensor)
        zone_color = get_color.get_mean_back_color(zone_color_sensor)
        if zone_color in mapwhite:
            if front_color in mapred:
                leftmotor.set_power(8)
                rightmotor.set_power(35)
            elif front_color in mapblue: 
                leftmotor.set_power(35)
                rightmotor.set_power(8)
            else:
                leftmotor.set_power(19)
                rightmotor.set_power(19)
        else:
            leftmotor.set_power(0)
            rightmotor.set_power(0)
            delivery = read()
            delivery_colors.append(delivery)
            drop(delivery)
            while zone_color in mapwhite:
                zone_color = get_color.get_mean_back_color(zone_color_sensor)
                leftmotor.set_power(19)
                rightmotor.set_power(19)
    except BaseException as error:
        print(error)

# Main function
time.sleep(4)
try:
    while not sensor.is_pressed():
        follow_path()
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()