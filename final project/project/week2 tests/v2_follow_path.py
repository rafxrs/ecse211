"""
Newer version of the follow_path code
This uses the new files wwe created instead of redefining the functions inside of the code
We now have the get_mean_color function inside of the get_color file in the colors folder
The emergency stop function is in utils.emergency_stop
"""
from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
import time
from colors import get_color

leftmotor = Motor("D")
rightmotor = Motor("A")
color_sensor = EV3ColorSensor(3)
sensor = TouchSensor(1)

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]
delivery_zones = ["red_zone", "orange_zone", "green_zone", "blue_zone", "purple_zone"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]

wait_ready_sensors(True)
print("Done waiting.")

def follow_path():
    try:
        path_color= get_color.get_mean_color(color_sensor)
        if path_color in mapred:
            leftmotor.set_power(8)
            rightmotor.set_power(35)
        elif path_color in mapblue: 
            leftmotor.set_power(35)
            rightmotor.set_power(8)
        else:
            leftmotor.set_power(18)
            rightmotor.set_power(18)
    
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