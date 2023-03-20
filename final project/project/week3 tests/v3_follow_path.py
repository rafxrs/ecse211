"""
CODE IN PROGRESS

Third version of the follow path algorithm
In this version, we use two color sensors, one far ahead of the robot to follow the path accurately
The second color sensor is parallel to the wheels on the robot and its role is to detect the green line
If the green line is detected, the goal is to perform a 90° right turn, read the color, and a 90° turn left
This is all done in this file
Four different tests were performed:
- 90° turn left and right --> function turn(direction)
- 90° turn when green is detected --> functions turn(direction) and follow_path()
- 90° turn when green is detected + read the color --> functions turn(direction), read() and follow_path()
- 90° turn when green is detected, read the color, and 90° turn left --> functions turn(direction), read() and follow_path()
"""

from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
import time
from colors import get_color

leftmotor = Motor("D")
rightmotor = Motor("A")
path_color_sensor = EV3ColorSensor(3)
wheel_color_sensor = EV3ColorSensor(2)
sensor = TouchSensor(1)

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]

wait_ready_sensors(True)
print("Done waiting.")


def turn(direction):
    if direction == "right":
        leftmotor.set_position_relative(360)
        rightmotor.set_position_relative(-180)
    elif direction == "left":
        leftmotor.set_position_relative(-180)
        rightmotor.set_position_relative(360)
    else:
        pass
    time.sleep(1)

#def read():



def follow_path():
    try:
        path_color= get_color.get_mean_color(path_color_sensor)
        wheel_color= get_color.get_mean_color(wheel_color_sensor)

        if wheel_color not in mapgreen:
            if path_color in mapred:
                leftmotor.set_power(8)
                rightmotor.set_power(35)
            elif path_color in mapblue: 
                leftmotor.set_power(35)
                rightmotor.set_power(8)
            else:
                leftmotor.set_power(18)
                rightmotor.set_power(18)
        else:
            leftmotor.set_power(0)
            rightmotor.set_power(0)
            turn("right")
            ES.emergency_stop()
    
    except BaseException as error:
        print(error)


# Main function
time.sleep(4)
try:
    while not sensor.is_pressed():
        turn("right")
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()