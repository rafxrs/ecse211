from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
from collections import deque
from colors import color_info, get_color, rgb
import time, math


leftmotor = Motor("D")
rightmotor = Motor("A")
blue_color_sensor = EV3ColorSensor(3)
red_color_sensor = EV3ColorSensor(2)
sensor = TouchSensor(1)
sleepsensor = TouchSensor(4)

wait_ready_sensors(True)
print("Done waiting.")

colors_dict = color_info.get_cd()

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]
delivery_zones = ["red_zone", "orange_zone", "green_zone", "blue_zone", "purple_zone"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]


# Define the threshold for color distance
color_threshold = 50



# Define the function to calculate the distance between two colors
def color_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    normalized_r1, normalized_g1, normalized_b1 = rgb.normalize_rgb(r1, g1, b1)
    normalized_r2, normalized_g2, normalized_b2 = rgb.normalize_rgb(r2, g2, b2)
    distance = math.sqrt((normalized_r1 - normalized_r2)**2 +
                         (normalized_g1 - normalized_g2)**2 +
                         (normalized_b1 - normalized_b2)**2)
    return distance

# Define the function to get the closest color
def closest_color(rgb_values):
    min_distance = float('inf')
    closest_color = None
    for color_name, color_values in colors_dict.items():
        distance = color_distance(rgb_values, color_values["mean"])
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    if min_distance < color_threshold:
        return closest_color
    else:
        return None

blue_color_polls = deque(maxlen=10)

def blue_mean_color(color_name):
    
    blue_color_polls.append(color_name)
    #print(len(color_polls))
    if len(blue_color_polls) == 10:
        color_counts= {}
        for color in blue_color_polls:
            if color in color_counts:
                color_counts[color]+=1
            else:
                color_counts[color]=1
        mode_color = max(color_counts, key=color_counts.get)
        return mode_color
    else:
        return "unknown"

red_color_polls = deque(maxlen=10)

def red_mean_color(color_name):
    
    red_color_polls.append(color_name)
    #print(len(color_polls))
    if len(red_color_polls) == 10:
        color_counts= {}
        for color in red_color_polls:
            if color in color_counts:
                color_counts[color]+=1
            else:
                color_counts[color]=1
        mode_color = max(color_counts, key=color_counts.get)
        return mode_color
    else:
        return "unknown"

last_30 = deque(maxlen=30)

def get_last_30(mean):
    last_30.append(mean)
    #print(len(color_polls))
    if len(last_30) == 30:
        last_counts= {}
        for color in last_30:
            if color in last_counts:
                last_counts[color]+=1
            else:
                last_counts[color]=1
        last_color = max(last_counts, key=last_counts.get)
        return last_color
    else:
        return "unknown"
    
def get_blue_sensor():
    color = closest_color(tuple(blue_color_sensor.get_rgb()))
    #print(color)
    mean = blue_mean_color(color)
    #print("mean: "+mean)
    return mean

def get_red_sensor():
    mobile_color = closest_color(tuple(red_color_sensor.get_rgb()))
    #print(color)
    mean_red = red_mean_color(mobile_color)
    #print("mean right: "+mean_red)
    return mean_red

# def get_delivery_zone():
#         return get_red_sensor()

#def adjust_robot():


def follow_path():
    try:
        blue_path = get_blue_sensor()
        red_path = get_red_sensor()
        
        #last = get_last_30(blue_path)
        #print("last 30 mean: "+last)
        #print(color_sensor.get_rgb())

        if blue_path in mapblue:
            leftmotor.set_power(8)
            rightmotor.set_power(30)
        elif (blue_path in mapgreen):
            leftmotor.set_power(0)
            rightmotor.set_power(0)
            #adjust_robot()
            delivery_color = red_path
            print("color: "+ delivery_color)
            time.sleep(1)
            while blue_path in mapgreen:
                blue_path = get_blue_sensor()
                leftmotor.set_power(30)
                rightmotor.set_power(8)

        else:
            #print("No movement")
            leftmotor.set_power(30)
            rightmotor.set_power(8)
    
    except BaseException as error:
        print(error)


        
time.sleep(4)
try:
    while not sensor.is_pressed():
        follow_path()
        #print(color_sensor.get_rgb())
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()

