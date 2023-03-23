"""
CODE IN PROGRESS

Fifth version of the follow path algorithm
In this version, we use two color sensors, one far ahead of the robot to follow the path accurately
The second color sensor is static and on top of the delivery zone and its role is to detect the delivery color

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
lap = 0

POWER_LIMIT = 40       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

slidemotor.reset_encoder()                      # Reset encoder to 0 value
slidemotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
slidemotor.set_power(0)

pushmotor.reset_encoder()                      # Reset encoder to 0 value
pushmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
pushmotor.set_power(0)

wait_ready_sensors(True)
print("Done waiting.")

# amount we need to move to get to next position
step = 98.3


# We changed the initial position to be yellow because that makes the weight distribution better
cube_positions = {
    "red": -196.60,
    "orange": -98.3,
    "yellow": 0,
    "green": 98.3,
    "blue": 196.60,
    "purple": 294.9
}

# Move to a specific cube position: works with color name
def move_to_cube_position(color_name):
    position = cube_positions[color_name] 
    slidemotor.set_position_relative(position)
    time.sleep(2)

# Move back to base position (yellow) from current color position
def move_to_base(current_color):
    position = cube_positions[current_color]
    slidemotor.set_position_relative((-1)*(position))
    time.sleep(2)

# Push the cube
def push():
    pushmotor.set_position_relative(360)
    time.sleep(2)

def drop(color):
    """
    Drops the cube of color 'color'
    First, we slide to get the right position
    Then, we push
    """
    move_to_cube_position(color)
    time.sleep(1)
    push()
    move_to_base(color)

def turn_around():
    """
    Function to turn the robot around 180 degrees
    Code in progress
    """

def request_new_cubes():
    """
    Code to play sound sequence to request new cubes for second round
    Code in progress
    """

def follow_path_backwards():
    """
    Function to follow the path backwards after the first run
    Code in progress"""
    path_color= get_color.get_mean_color(front_color_sensor)
    last = get_color.get_last_20(path_color)

    if path_color == "yellow":
        turn_around()
        request_new_cubes()

    elif path_color in mapblue:
        leftmotor.set_power(-15)
        rightmotor.set_power(45)
    elif path_color in mapred: 
        leftmotor.set_power(45)
        rightmotor.set_power(-15)
    elif path_color in mapgreen:
        if last in mapred: # if we were seeing red before we reached green, need to keep going right
            leftmotor.set_power(-10)
            rightmotor.set_power(35)
        elif last in mapblue:  # if we were seeing blue before we reached green, need to keep going left
            leftmotor.set_power(15)
            rightmotor.set_power(-5)
        else:
            leftmotor.set_power(10)
            rightmotor.set_power(10)
    else:
        leftmotor.set_power(10)
        rightmotor.set_power(10)


def follow_path_carefully():
    """
    To follow the path slowly, only with the front sensor:
    We need this function when the back sensor reads the zone color and when we reach the green line
    If we only use follow_path(), when the back sensor sees green, it will keep turning right and left and read the delivery color
    """
    path_color= get_color.get_mean_color(front_color_sensor)
    if path_color in mapred:
        leftmotor.set_power(-5)
        rightmotor.set_power(15)
    elif path_color in mapblue: 
        leftmotor.set_power(35)
        rightmotor.set_power(-10)
    else:
        leftmotor.set_power(10)
        rightmotor.set_power(10)
    

def follow_path():
    """
    Fifth version of follow path.
    The algorithm is as follows:
    If we see red, drive left
    If we see blue, drive right
    If we see the green line, we carefully keep driving, slowly, until the colour sensor on the right reads the delivery color
    When the colour sensor reads a delivery colour, we keep driving a tiny bit in order to position the drop cage over the zone.
    Then, we select and drop the corresponding cube, and keep driving and repeating those previous steps
    """
    
    try:
        # This code is to check whether all cubes were delivered or not (not using this feature yet)
        # if len(delivery_cubes)==0:
        #     delivery_cubes.append("red")
        #     delivery_cubes.append("orange")
        #     delivery_cubes.append("yellow")
        #     delivery_cubes.append("green")
        #     delivery_cubes.append("blue")
        #     delivery_cubes.append("purple")
        #     lap+=1
        
        # Get the front color sensor data
        path_color= get_color.get_mean_color(front_color_sensor)
        print("The path is "+path_color)
        zone_color = get_color.get_mean_zone_color(zone_color_sensor)
        last = get_color.get_last_10(path_color)
        print("LAST IS "+ last)
        
        if path_color in mapred:
            leftmotor.set_power(-15)
            rightmotor.set_power(45)

        elif path_color in mapblue: 
            leftmotor.set_power(45)
            rightmotor.set_power(-15)

        elif path_color in mapgreen:
            # We reached a green line so we know there is a delivery zone close
            leftmotor.set_power(0)
            rightmotor.set_power(0)

            # Need to drive carefully and slowly
            while path_color in mapgreen:
                zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                path_color= get_color.get_mean_color(front_color_sensor)
                if last in mapred: # if we were seeing red before we reached green, need to keep going left
                    leftmotor.set_power(-5)
                    rightmotor.set_power(15)
                elif last in mapblue:  # if we were seeing blue before we reached green, need to keep going right
                    leftmotor.set_power(35)
                    rightmotor.set_power(-10)
                else:
                    leftmotor.set_power(10)
                    rightmotor.set_power(10)
            # If we stop seeing the green line, that means we're even closer to the zone, and now we drive
            # carefully until our colour sensor on the right reaches the delivery zone
            while zone_color not in delivery_cubes:
                zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                path_color= get_color.get_mean_color(front_color_sensor)
                follow_path_carefully()

            # After we reached the delivery zone, we carefully continue to follow the path for x seconds
            # This is done right below and it is done to position the drop cage perfectly over the zone
            t = 0
            while t<1.7:
                time.sleep(0.1)
                follow_path_carefully()
                t+=0.1

            # The cage should now be over the delivery zone. We stop all motion, read the colour value, and drop the cube
            leftmotor.set_power(0)
            rightmotor.set_power(0)

            zone_color = get_color.get_mean_zone_color(zone_color_sensor)
            time.sleep(2)
            # mean_zone_color = get_color.get_last_20(zone_color)
            
            # Print the delivery zone for testing purposes, and drop the cube
            print("ZONE IS "+zone_color)
            drop(zone_color)
            print("DROPPED "+zone_color)

            # delivery_cubes.remove(zone_color)
            color_read = zone_color

            # While we're over the delivery zone, we can't turn too hard and need to keep driving carefully until we're out of reach
            while zone_color == color_read:
                zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                path_color= get_color.get_mean_color(front_color_sensor)
                follow_path_carefully()
        
        # If we don't see red, or blue, or green, we are seeing the white line in the middle, and we can drive straight
        else:
            leftmotor.set_power(18)
            rightmotor.set_power(21)
    
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