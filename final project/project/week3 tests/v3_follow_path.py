"""
CODE IN PROGRESS

Third version of the follow path algorithm
In this version, we use two color sensors, one far ahead of the robot to follow the path accurately
The second color sensor is parallel to the wheels on the robot and its role is to detect the green line
If the green line is detected, the goal is to perform a 90° right turn, read the color, and a 90° turn left
This is all done in this file
Four different tests:
- 90° turn left and right --> function turn(direction)
- 90° turn when green is detected --> functions turn(direction) and follow_path()
- 90° turn when green is detected + adjust robot by driving backwards + read the color --> functions turn(direction), drive_backwards() and follow_path()
- 90° turn when green is detected, read the color, adjust, 90° turn left, adjust, keep driving --> functions turn(direction), drive_backwards(), drive_forward(), read() and follow_path()
"""

from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
import time
from colors import get_color

leftmotor = Motor("D")
rightmotor = Motor("A")
front_color_sensor = EV3ColorSensor(3)
back_color_sensor = EV3ColorSensor(2)
sensor = TouchSensor(1)

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]

wait_ready_sensors(True)
print("Done waiting.")

POWER_LIMIT = 40       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

def turn(direction):
    leftmotor.reset_encoder()                      # Reset encoder to 0 value
    leftmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    rightmotor.reset_encoder()                      # Reset encoder to 0 value
    rightmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits

    if direction == "right":
        leftmotor.set_position_relative(205)
        rightmotor.set_position_relative(-198)
    elif direction == "left":
        leftmotor.set_position_relative(-198)
        rightmotor.set_position_relative(205)
    else:
        pass
    time.sleep(2)

def drive_backwards():
    """
    Drive slighly backwards
    """
    leftmotor.reset_encoder()                      # Reset encoder to 0 value
    leftmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    rightmotor.reset_encoder()                      # Reset encoder to 0 value
    rightmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    leftmotor.set_position_relative(-90)
    rightmotor.set_position_relative(-90)

def drive_forward():
    """
    Drive slightly forward
    """
    leftmotor.reset_encoder()                      # Reset encoder to 0 value
    leftmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    rightmotor.reset_encoder()                      # Reset encoder to 0 value
    rightmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    leftmotor.set_position_relative(90)
    rightmotor.set_position_relative(90)
    time.sleep(1)

def follow_path_without_back_sensor():
    """
    To follow the path only with the front sensor:
    We need this function when the back sensor reads green
    If we only use follow_path(), when the back sensor sees green, it will keep turning right and left and read the delivery color
    We need to get to the next green line, so if we need to ignore the back sensor and keep driving we can use this function
    """
    front_color= get_color.get_mean_front_color(front_color_sensor)
    if front_color in mapred:
        leftmotor.set_power(8)
        rightmotor.set_power(35)
    elif front_color in mapblue: 
        leftmotor.set_power(35)
        rightmotor.set_power(8)
    else:
        leftmotor.set_power(18)
        rightmotor.set_power(18)

def follow_path():
    """
    Follows the path
    If back sensor reads green, robot adjusts itslef (turns right, then backwards, then reads color, then turns left, then drives forward)
    Then the robot keeps driving until the next green line
    """
    try:
        
        delivery_colors = []

        front_color= get_color.get_mean_front_color(front_color_sensor)
        back_color= get_color.get_mean_back_color(back_color_sensor)
        #last = get_color.get_last_20(wheel_color)
        
        if back_color not in mapgreen:
            if front_color in mapred:
                leftmotor.set_power(-3)
                rightmotor.set_power(45)
            elif front_color in mapblue: 
                leftmotor.set_power(45)
                rightmotor.set_power(-3)
            else:
                leftmotor.set_power(25)
                rightmotor.set_power(25)
        else:
            leftmotor.set_power(0)
            rightmotor.set_power(0)
            drive_forward()
            turn("right")
            time.sleep(1)
            drive_backwards()
            delivery_colors.append(front_color)
            turn("left")
            drive_forward()
            while back_color in mapgreen:
                back_color= get_color.get_mean_back_color(back_color_sensor)
                follow_path_without_back_sensor()


    
    except BaseException as error:
        print(error)


# Main function
time.sleep(4)
try:
    while not sensor.is_pressed():
        # Comment out the lines you don't want to test

        # turn("right")
        # drive_backwards()
        
        # turn("left")
        # drive_forward()
        
        follow_path()
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()