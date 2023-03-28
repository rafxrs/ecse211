"""
CODE IN PROGRESS
v5.3
Added function full_lap() to follow the path and drop cubes while there are still cubes to drop,
stop the robot when all cubes are delivered, turn around 180 degrees and drive back to the base.

This code works on the map used for the demo (the one with the u-turn)
Does NOT work on counterclockwise medium map due to need for adjuste=ment when we reach the green line
This is to be added on 03.28 in the version 5.4

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

"""
CONSTANTS
"""

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

"""
INITIALIZE MOTORS
"""

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



def turn_around():
    """
    v5.1
    Function to perform a 180 turn when we finish the track
    """
    t = 0
    leftmotor.set_power(15)
    rightmotor.set_power(15)
    while t<0.5:
        time.sleep(0.1)
        t+=0.1
    t = 0
    leftmotor.set_power(-25)
    rightmotor.set_power(10)
    while t<1:
        time.sleep(0.1)
        t+=0.1
    t = 0
    leftmotor.set_power(0)
    rightmotor.set_power(30)
    while t<1.5:
        time.sleep(0.1)
        t+=0.1
    t = 0
    leftmotor.set_power(-25)
    rightmotor.set_power(10)
    while t<2:
        time.sleep(0.1)
        t+=0.1
    leftmotor.set_power(0)
    rightmotor.set_power(0)

    print("Done")
    time.sleep(4)


def follow_path_backwards():
    """
    v5.2
    Function to follow the path on the way back to the loading bay
    """
    global green
    color = get_color.get_mean_color(front_color_sensor)

    if green == 6 and color == "yellow":
        ES.emergency_stop()
        
    if color in mapblue:
        leftmotor.set_power(-20)
        rightmotor.set_power(65)

    elif color in mapred: 

        leftmotor.set_power(45)
        rightmotor.set_power(-15)

    elif color in mapgreen:

        green+=1
        print(green)
        while color in mapgreen:
            color= get_color.get_mean_color(front_color_sensor)
            follow_path_carefully()
    else:
        leftmotor.set_power(20)
        rightmotor.set_power(20)



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
    To follow the path only with the front sensor:
    We need this function when the back sensor reads the zone color
    If we only use follow_path(), when the back sensor sees green, it will keep turning right and left and read the delivery color
    We need to get to the next green line, so if we need to ignore the back sensor and keep driving we can use this function
    """
    path_color= get_color.get_mean_color(front_color_sensor)
    if path_color in mapred:
        leftmotor.set_power(-5)
        rightmotor.set_power(15)
    elif path_color in mapblue: 
        leftmotor.set_power(20)
        rightmotor.set_power(-10)
    else:
        leftmotor.set_power(12)
        rightmotor.set_power(12)
    

def follow_path():
    """
    Follow the path, slow down when green line is reached, get delivery color, drive carefully, drop cube, keep going
    """
    try:
        
        # if len(delivery_cubes)==0:
        #     delivery_cubes.append("red")
        #     delivery_cubes.append("orange")
        #     delivery_cubes.append("yellow")
        #     delivery_cubes.append("green")
        #     delivery_cubes.append("blue")
        #     delivery_cubes.append("purple")
        
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

# Global variable to keep track of how many green lines were seen on the way back to the loading bay
green = 0
def full_lap():
    """
    v5.3
    """
    while not len(delivery_cubes)==0 and not sensor.is_pressed():
        follow_path()
    if sensor.is_pressed(): ES.emergency_stop()
    turn_around()
    while not sensor.is_pressed():
        follow_path_backwards()

# Main function
time.sleep(4)
try:
    while not sensor.is_pressed():
        full_lap()
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()