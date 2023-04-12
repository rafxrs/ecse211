"""
Code used for demo on 23/03: works on the u turn map
v5 of follow path

Major changes from v4:
    - added follow_path_carefully() to drive the robot carefully when we rach the line/approach the zone

In this version, we use two color sensors, one in front of the robot to follow the path accurately
The second color sensor is static and on top of the delivery zone and its role is to detect the delivery color
If the green line is detected, the goal is to keep driving unitl we have the wheels on the green zone (or until the second color sensor reads a delivery zone value)
This is all done in this file
We stop the robot after all 6 cubes have been delivered
"""
from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
import time
from colors import get_color

leftmotor = Motor("D")
rightmotor = Motor("A")
pushmotor= Motor("C")
slidemotor = Motor("B")
front_color_sensor = EV3ColorSensor(3)
zone_color_sensor = EV3ColorSensor(2)
sensor = TouchSensor(1)

# Names of the colors
mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]
delivery_zones = []

POWER_LIMIT = 40       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

# amount we need to move to get to next position
step = 98.3
cube_positions = {
    "red": -196.60,
    "orange": -98.3,
    "yellow": 0,
    "green": 98.3,
    "blue": 196.60,
    "purple": 294.9
}

slidemotor.reset_encoder()                      # Reset encoder to 0 value
slidemotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
slidemotor.set_power(0)

pushmotor.reset_encoder()                      # Reset encoder to 0 value
pushmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
pushmotor.set_power(0)

leftmotor.reset_encoder() 
rightmotor.reset_encoder() 


# Initialize sensors
wait_ready_sensors(True)
print("Done waiting.")

def move_to_cube_position(color_name):
    """
    Imported from v4
    Move to a specific cube position on the conveyor belt
    """
    position = cube_positions[color_name] 
    slidemotor.set_position_relative(position)
    time.sleep(2)

def move_to_base(current_color):
    """
    Imported from v4
    Move to a base position on the conveyor belt, from current position 'color'
    """
    position = cube_positions[current_color]
    slidemotor.set_position_relative((-1)*(position))
    time.sleep(2)

def push():
    """
    Imported from v4
    Function to activate the piston
    """
    pushmotor.set_position_relative(360)
    time.sleep(2)

def drop(color):
    """
    Imported from v4
    Drops the cube of color 'color'
    First, we slide to get the right position
    Then, we push
    Then, we move back to initial position
    """
    move_to_cube_position(color)
    pushmotor.set_limits(80, 500) # Set the power and speed limits
    # Push twice to make sure the cube falls off
    push()
    push()
    pushmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    move_to_base(color)
    

def follow_path_carefully():
    """
    New in v5
    """
    path_color= get_color.get_mean_color(front_color_sensor)
    if path_color in mapred:
        leftmotor.set_power(-14)
        rightmotor.set_power(20)
    elif path_color in mapblue: 
        leftmotor.set_power(23)
        rightmotor.set_power(-14)
    elif path_color in mapgreen:
        leftmotor.set_power(14)
        rightmotor.set_power(14)
    else:
        leftmotor.set_power(10)
        rightmotor.set_power(14)
    

def follow_path():
    """
    Follow the path, slow down when green line is reached, get delivery color, drive carefully, drop cube, keep going
    """
    try:
        
        path_color= get_color.get_mean_color(front_color_sensor)
        zone_color = get_color.get_mean_zone_color(zone_color_sensor)
        
        if path_color in mapred:
            leftmotor.set_power(-20)
            rightmotor.set_power(55)

        elif path_color in mapblue: 
            leftmotor.set_power(45)
            rightmotor.set_power(-15)

        elif path_color in mapgreen:
            leftmotor.set_power(0)
            rightmotor.set_power(0)
            
            while path_color in mapgreen:
                zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                path_color= get_color.get_mean_color(front_color_sensor)
                follow_path_carefully()
            while zone_color not in delivery_cubes:
                zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                path_color= get_color.get_mean_color(front_color_sensor)
                follow_path_carefully()

            t = 0
            delivery_color = zone_color
            while t<3.2:
                time.sleep(0.1)
                follow_path_carefully()
                t+=0.1
            leftmotor.set_power(0)
            rightmotor.set_power(0)

            print("ZONE IS "+delivery_color)
            drop(delivery_color)
            print("DROPPED "+delivery_color)
            delivery_cubes.remove(zone_color)

            while zone_color == delivery_color:
                zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                path_color= get_color.get_mean_color(front_color_sensor)
                follow_path_carefully()
            


            
        else:
            leftmotor.set_power(18)
            rightmotor.set_power(20)
    
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