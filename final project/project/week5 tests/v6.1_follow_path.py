"""
CODE IN PROGRESS
v6
FINAL VERSION


"""

from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
import time
from colors import get_color
from utils.sound import Sound

more = Sound(duration=3.0, volume=100, pitch="E4")
leftmotor = Motor("D")
rightmotor = Motor("A")
pushmotor= Motor("C")
slidemotor = Motor("B")
front_color_sensor = EV3ColorSensor(3)
zone_color_sensor = EV3ColorSensor(2)
sensor = TouchSensor(1)
startsensor = TouchSensor(4)

"""
CONSTANTS
"""

# Names of the colors
mapred = ["map_red", "map_red_plus_tape", "red", "redfront"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue", "bluefront"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]
mapyellow = ["yellow", "yellowfront"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]
delivery_zones = []

#Global variable to keep track of what turn we were taking last
last = "white"
last_backwards = "white"
yellow = False
adjusted = False

#Global variable for the delivery color
delivery_color = ""

POWER_LIMIT = 40       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

POWER_LIMIT_PISTON = 20       # Power limit (percentage)
SPEED_LIMIT_PISTON = 180      # Speed limit in degree per second

# amount we need to move to get to next position
step = 98.3
cube_positions = {
    "red": 0,
    "orange": 98.3,
    "yellow": 196.60,
    "green": 290,
    "blue": 380,
    "purple": 491.5
}

"""
INITIALIZE MOTORS
"""

slidemotor.reset_encoder()                      # Reset encoder to 0 value
slidemotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
slidemotor.set_power(0)

pushmotor.reset_encoder()                      # Reset encoder to 0 value
pushmotor.set_limits(POWER_LIMIT_PISTON, SPEED_LIMIT_PISTON) # Set the power and speed limits
pushmotor.set_power(0)

leftmotor.reset_encoder() 
rightmotor.reset_encoder() 


# Initialize sensors
wait_ready_sensors(True)
print("Done waiting.")

def play_sound(sound):
    #Play a single note.
    sound.play()
    sound.wait_done()

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
        while t<1:
            time.sleep(0.1)
            t+=0.1

        last = "white"
        t=0
        leftmotor.set_power(0)
        rightmotor.set_power(20)
        while t<0.8:
            time.sleep(0.1)
            t+=0.1

    elif last_backwards=="red":
        path_color = get_color.get_mean_front_color(front_color_sensor)
        while path_color in mapgreen:
            path_color = get_color.get_mean_front_color(front_color_sensor)
            leftmotor.set_power(-15)
            rightmotor.set_power(-15)
        
        t=0
        leftmotor.set_power(-15)
        rightmotor.set_power(-15)
        while t<0.5:
            time.sleep(0.1)
            t+=0.1

        last_backwards = "white"
        t=0
        leftmotor.set_power(20)
        rightmotor.set_power(-20)
        while t<0.7:
            time.sleep(0.1)
            t+=0.1

def turn_around():
    """
    v5.1
    Function to perform a 180 turn when we finish the track
    """
    
    leftmotor.set_power(20)
    rightmotor.set_power(20)
    time.sleep(1)
    
    leftmotor.set_power(-35)
    rightmotor.set_power(40)
    time.sleep(2)
    # t = 0
    # leftmotor.set_power(-20)
    # rightmotor.set_power(40)
    # while t<1:
    #     time.sleep(0.1)
    #     t+=0.1
    # t = 0
    # leftmotor.set_power(-35)
    # rightmotor.set_power(15)
    # while t<1:
    #     time.sleep(0.1)
    #     t+=0.1
    # leftmotor.set_power(0)
    # rightmotor.set_power(0)
    # t = 0
    # leftmotor.set_power(15)
    # rightmotor.set_power(15)
    # while t<0.5:
    #     time.sleep(0.1)
    #     t+=0.1
    # leftmotor.set_power(2)
    # rightmotor.set_power(2)

    print("Done")
    # time.sleep(4)


def follow_path_backwards():
    """
    v5.2
    Function to follow the path on the way back to the loading bay
    """
    global last_backwards
    global last
    global green
    global yellow

    if len(delivery_cubes)==0:
            delivery_cubes.append("red")
            delivery_cubes.append("orange")
            delivery_cubes.append("yellow")
            delivery_cubes.append("green")
            delivery_cubes.append("blue")
            delivery_cubes.append("purple")


    color = get_color.get_mean_color(front_color_sensor)
    if green >= 6 and color in mapyellow:
        yellow = True

        
        
    elif color in mapblue:
        last_backwards="blue"
        leftmotor.set_power(-20)
        rightmotor.set_power(45)

    elif color in mapred: 
        last_backwards="red"
        leftmotor.set_power(45)
        rightmotor.set_power(-25)

    elif color in mapgreen:
        last = "white"
        if last_backwards == "red":
            green-=1
        adjust()
        green+=1
        print(green)
        while color in mapgreen:
            color= get_color.get_mean_color(front_color_sensor)
            follow_path_carefully()

    else:
        leftmotor.set_power(26)
        rightmotor.set_power(24)



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
    slidemotor.set_position_relative((-1)*(98.3*5))

def push():
    """
    Imported from v4
    Function to activate the piston
    """
    pushmotor.set_position_relative(362)
    time.sleep(1)

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
    # Push twice to make sure the cube falls off
    push()
    move_to_base(delivery_color)
    delivery_cubes.remove(delivery_color)
    
    

def follow_path_carefully():
    """
    To follow the path only with the front sensor:
    We need this function when the back sensor reads the zone color
    If we only use follow_path(), when the back sensor sees green, it will keep turning right and left and read the delivery color
    We need to get to the next green line, so if we need to ignore the back sensor and keep driving we can use this function
    """
    path_color= get_color.get_mean_color(front_color_sensor)
    if path_color in mapred:
        leftmotor.set_power(-12)
        rightmotor.set_power(18)
    elif path_color in mapblue: 
        leftmotor.set_power(18)
        rightmotor.set_power(-12)
    elif path_color in mapgreen:
        leftmotor.set_power(12)
        rightmotor.set_power(12)
    else:
        leftmotor.set_power(8)
        rightmotor.set_power(14)
    

def follow_path():
    """
    Follow the path, slow down when green line is reached, get delivery color, drive carefully, drop cube, keep going
    """
    try:
        # time.sleep(0.01)
        global delivery_color
        global last
        global adjusted
        
        path_color= get_color.get_mean_color(front_color_sensor)
        # zone_color = get_color.get_mean_zone_color(zone_color_sensor)
        
        if path_color in mapred:
        
            last = "red"
            leftmotor.set_power(-40)
            rightmotor.set_power(20)

        elif path_color in mapblue: 
        
            last = "blue"
            leftmotor.set_power(45)
            rightmotor.set_power(-15)

        elif path_color in mapgreen:
            if adjusted==False:
                find_placement()
            else:
                while path_color in mapgreen:
                    zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                    path_color= get_color.get_mean_color(front_color_sensor)
                    follow_path_carefully()
                while zone_color not in delivery_cubes:
                    zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                    path_color= get_color.get_mean_color(front_color_sensor)
                    follow_path_carefully()

                #Get the zone color sensor in the perfect position
                #t = 0
                #while t<0.1:
                #    time.sleep(0.1)
                #    follow_path_carefully()
                #    t+=0.01
                leftmotor.set_power(0)
                rightmotor.set_power(0)
                time.sleep(0.1)
                zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                delivery_color = zone_color
                while zone_color == "white":
                    zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                    delivery_color = zone_color

                

                while zone_color in delivery_cubes:
                    follow_path_carefully()
                    zone_color = get_color.get_mean_zone_color(zone_color_sensor)
                    path_color= get_color.get_mean_color(front_color_sensor)

                #t = 0
                #leftmotor.set_power(6)
                #rightmotor.set_power(8)
                #while t<0.01:
                #    time.sleep(0.01)
                #    t+=0.01
                leftmotor.set_power(0)
                rightmotor.set_power(0)

                print("ZONE IS "+delivery_color)
                drop()
                delivery_zones.append(delivery_color)
                
                if path_color in mapgreen:
                    while path_color in mapgreen:
                        path_color= get_color.get_mean_color(front_color_sensor)
                        follow_path_carefully()
                
                adjusted = False
                
        
                #adjust_after_green()
                    

                #last= "red"
            
        else:
            # last = "white"
            leftmotor.set_power(32)
            rightmotor.set_power(34)
    
    except BaseException as error:
        print(error)

# Global variable to keep track of how many green lines were seen on the way back to the loading bay
green = 0

def find_placement():

    global adjusted

    leftmotor.set_power(-30)
    rightmotor.set_power(-30)
    time.sleep(0.4)
    leftmotor.set_power(0)
    rightmotor.set_power(0)
    path_color= get_color.get_mean_color(front_color_sensor)
    while path_color not in mapred:
        path_color= get_color.get_mean_color(front_color_sensor)
        leftmotor.set_power(38)
        rightmotor.set_power(-10)
        if path_color in mapgreen:
            path_color= get_color.get_mean_color(front_color_sensor)
            leftmotor.set_power(-30)
            rightmotor.set_power(-30)
            time.sleep(0.02)

    while path_color not in mapblue:
        path_color= get_color.get_mean_color(front_color_sensor)
        leftmotor.set_power(-10)
        rightmotor.set_power(38)
        if path_color in mapgreen:
            path_color= get_color.get_mean_color(front_color_sensor)
            leftmotor.set_power(-30)
            rightmotor.set_power(-30)
            time.sleep(0.02)
                
    #t=0
    #leftmotor.set_power(40)
    #rightmotor.set_power(-10)
    #while t<0.2:
    #    time.sleep(0.1)
    #    t+=0.1
    
    leftmotor.set_power(10)
    rightmotor.set_power(-25)

    while path_color not in mapwhite:
        path_color= get_color.get_mean_color(front_color_sensor)
        leftmotor.set_power(15)
        rightmotor.set_power(-35)
        time.sleep(0.06)
        if path_color in mapgreen:
            path_color= get_color.get_mean_color(front_color_sensor)
            leftmotor.set_power(-30)
            rightmotor.set_power(-30)
        leftmotor.set_power(20)
        rightmotor.set_power(-35)

    adjusted = True

def full_lap():
    """
    v5.3
    """
    global yellow
    
    while not len(delivery_cubes)==0 and not sensor.is_pressed():
        follow_path()
    if sensor.is_pressed(): ES.emergency_stop()
    turn_around()
    while not sensor.is_pressed():
        if yellow:
            break
        follow_path_backwards()

    print("back to base")
    turn_around()
    leftmotor.set_power(0)
    rightmotor.set_power(0)
    yellow = False
    #Ask for more cubes
    play_sound(more)
    # while not startsensor.is_pressed():
    #     print("waiting'")
    #     time.sleep(0.1)




# Main function
time.sleep(4)
try:
    # turn_around()
    while not sensor.is_pressed():
        while not startsensor.is_pressed():
            print("waiting")
            pass
        # wait until press
        full_lap()
        
        # follow_path()
        # follow_path_backwards()
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()