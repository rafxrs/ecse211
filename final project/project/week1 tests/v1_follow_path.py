""" 
Very first version of the software that analyzes the color sensor values, takes the mean of the 10 last polls
and drives accordingly 
This code works and follows the path perfectly fine
"""
from utils.brick import BP, TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
import time, math
from collections import deque
leftmotor = Motor("D")
rightmotor = Motor("A")
color_sensor = EV3ColorSensor(3)
sensor = TouchSensor(1)
wait_ready_sensors(True)
print("Done waiting.")

def emergency_stop():
    #if this function is called that means touch sensor 3 was pressed
    #we stop everything, reset the brick pi and print the emergency stop message, and exit the program
        print('Emergency stop triggered')
        BP.reset_all()
        exit()

"""
Dictionary to keep track of mean RGB values of each color
"""
colors = {
    "black": {"mean": [0, 0, 0]},
    "white": {"mean": [300, 300, 200]},
    "yellow": {"mean": [300, 200, 20]},
    "orange": {"mean": [240, 80, 50]},
    "purple": {"mean": [185, 35, 35]},
    "map_white": {"mean": [300, 260, 170]},
    "map_tape": {"mean": [190, 170, 100]},
    "blue": {"mean": [37,60,60]},
    "map_blue_plus_tape": {"mean": [45,50,52]},
    "red": {"mean": [245,38,18]},
    "map_red_plus_tape": {"mean": [250,45,30]},
    "green": {"mean": [37,100,20]},
    "map_green_plus_tape": {"mean": [50,120,30]},
    }
mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]

# Define the threshold for color distance
color_threshold = 50
# Define the function to normalize RGB values
def normalize_rgb(r, g, b):
    denominator = math.sqrt(r**2+g**2+b**2)
    if denominator == 0:
        return 0,0,0
    normalized_r = r / math.sqrt(r**2 + g**2 + b**2)
    normalized_g = g / math.sqrt(r**2 + g**2 + b**2)
    normalized_b = b / math.sqrt(r**2 + g**2 + b**2)
    return normalized_r, normalized_g, normalized_b

# Define the function to calculate the distance between two colors
def color_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    normalized_r1, normalized_g1, normalized_b1 = normalize_rgb(r1, g1, b1)
    normalized_r2, normalized_g2, normalized_b2 = normalize_rgb(r2, g2, b2)
    distance = math.sqrt((normalized_r1 - normalized_r2)**2 +
                         (normalized_g1 - normalized_g2)**2 +
                         (normalized_b1 - normalized_b2)**2)
    return distance

# Define the function to get the closest color
def closest_color(rgb_values):
    min_distance = float('inf')
    closest_color = None
    for color_name, color_values in colors.items():
        distance = color_distance(rgb_values, color_values["mean"])
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    if min_distance < color_threshold:
        return closest_color
    else:
        return None

color_polls = deque(maxlen=10)
def mean_color(color_name):
    color_polls.append(color_name)
    #print(len(color_polls))
    if len(color_polls) == 10:
        color_counts= {}
        for color in color_polls:
            if color in color_counts:
                color_counts[color]+=1
            else:
                color_counts[color]=1
        mode_color = max(color_counts, key=color_counts.get)
        return mode_color
    else:
        return "unknown"

def get_color():
    color = closest_color(tuple(color_sensor.get_rgb()))
    #print(color)
    mean = mean_color(color)
    print("mean: "+mean)
    return mean

def follow_path():
    try:
        path_color= get_color()
        if path_color == "yellow":
            leftmotor.set_power(12)
            rightmotor.set_power(12)
        elif path_color in mapred:
            leftmotor.set_power(8)
            rightmotor.set_power(30)
        elif path_color in mapblue: 
            leftmotor.set_power(30)
            rightmotor.set_power(8)
        else:
            leftmotor.set_power(12)
            rightmotor.set_power(12)
    except BaseException as error:
        print(error)
        
time.sleep(4)
try:
    while not sensor.is_pressed():
        follow_path()
    emergency_stop()
except BaseException as error:
    print(error)
    exit()