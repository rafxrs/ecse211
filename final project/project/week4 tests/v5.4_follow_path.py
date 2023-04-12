"""
v5.4

Changes from v5.3:
added a way to adjust the robot when we reach the green line 
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

#Global variable to keep track of what turn we were taking last
last = "white"

#Global variable for the delivery color
delivery_color = ""

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


def adjust():
    """
    New in v5.4
    Adjust the robot when we reach the green line depending on what turn we were taking previously
    """
    global last
    global last_backwards

    if last=="red":
        # Adjust if we saw red last
        path_color = get_color.get_mean_front_color(front_color_sensor)
        while path_color in mapgreen:
            path_color = get_color.get_mean_front_color(front_color_sensor)
            leftmotor.set_power(-15)
            rightmotor.set_power(-15)
        
        t=0
        leftmotor.set_power(-15)
        rightmotor.set_power(-15)
        while t<0.7:
            time.sleep(0.1)
            t+=0.1

        last = "white"
        t=0
        leftmotor.set_power(0)
        rightmotor.set_power(20)
        while t<0.7:
            time.sleep(0.1)
            t+=0.1

def turn_around():
    """
    v5.1
    Function to perform a 180 turn when we finish the track
    """
    t = 0
    leftmotor.set_power(-35)
    rightmotor.set_power(40)
    while t<1.8:
        time.sleep(0.1)
        t+=0.1

def follow_path_backwards():
    """
    v5.2
    Function to follow the path on the way back to the loading bay
    """
    global green
    color = get_color.get_mean_color(front_color_sensor)

    if green >= 6 and color == "yellow":
        ES.emergency_stop()
        
    if color in mapblue:

        leftmotor.set_power(-20)
        rightmotor.set_power(45)

    elif color in mapred: 

        leftmotor.set_power(45)
        rightmotor.set_power(-25)

    elif color in mapgreen:
        # adjust()
        time.sleep(1)
        green+=1
        print(green)
        while color in mapgreen:
            color= get_color.get_mean_color(front_color_sensor)
            follow_path_carefully()
    else:
        leftmotor.set_power(20)
        rightmotor.set_power(18)



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

def drop():
    """
    Imported from v4
    Drops the cube of color 'color'
    First, we slide to get the right position
    Then, we push
    """
    global delivery_cubes
    move_to_cube_position(delivery_color)
    pushmotor.set_limits(140, 1500) # Set the power and speed limits
    push()
    move_to_base(delivery_color)
    delivery_cubes.remove(delivery_color)
    
    

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
        global delivery_color
        global last
        
        path_color= get_color.get_mean_color(front_color_sensor)
        
        if path_color in mapred:
        
            last = "red"
            leftmotor.set_power(-20)
            rightmotor.set_power(55)

        elif path_color in mapblue: 
        
            last = "blue"
            leftmotor.set_power(45)
            rightmotor.set_power(-15)

        elif path_color in mapgreen:
            if last=="red":
                adjust()
            else:
                while path_color in mapgreen:
                    zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                    path_color= get_color.get_mean_color(front_color_sensor)
                    follow_path_carefully()
                while zone_color not in delivery_cubes:
                    zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                    path_color= get_color.get_mean_color(front_color_sensor)
                    follow_path_carefully()

                # Get the zone color sensor in the perfect position
                t = 0
                while t<0.8:
                    time.sleep(0.1)
                    follow_path_carefully()
                    t+=0.1
                leftmotor.set_power(0)
                rightmotor.set_power(0)
                zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                delivery_color = zone_color
                time.sleep(1)

                

                while zone_color in delivery_cubes:
                    zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                    path_color= get_color.get_mean_color(front_color_sensor)
                    follow_path_carefully()

                t = 0
                while t<0.5:
                    time.sleep(0.1)
                    follow_path_carefully()
                    t+=0.1
                leftmotor.set_power(0)
                rightmotor.set_power(0)

                print("ZONE IS "+delivery_color)
                drop()
                
                if path_color in mapgreen:
                    while path_color in mapgreen:
                        path_color= get_color.get_mean_color(front_color_sensor)
                        follow_path_carefully()

                

                last= "red"
            
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
    While there are cubes to deliver, follow the path
    When all cubes are delivered, turn around and drive back to bay
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
        #follow_path()
        #follow_path_backwards()
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()