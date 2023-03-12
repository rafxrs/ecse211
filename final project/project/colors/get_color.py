"""
This script implements the crucial function get_mean_color()
We poll the color sensor continuously, and normalize the rgb values. Then, we check the distance
to the closest color cluster to determine what color we are seeing.
For more precision, we take the last 10 polls and the color that appears the most in those 10 polls is the 
color we are currently seeing
"""


from colors import color_info
import math
from collections import deque

# Color dictionary
colors_dict = color_info.get_cd()

# Names of the colors
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
    for color_name, color_values in colors_dict.items():
        distance = color_distance(rgb_values, color_values["mean"])
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    if min_distance < color_threshold:
        return closest_color
    else:
        return None

# Queue to take the last 10 polls and then take the most common color 
color_polls = deque(maxlen=10)

# Function that returns the color that appears the most in the last ten polls
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

# Queue that takes the last 20 mean values
last_20 = deque(maxlen=20)

# Function that returns the mean color of the last 10 mean colors
# That is to say, this function takes 300 polls as input
def get_last_30(mean):
    last_20.append(mean)
    #print(len(color_polls))
    if len(last_20) == 30:
        last_counts= {}
        for color in last_20:
            if color in last_counts:
                last_counts[color]+=1
            else:
                last_counts[color]=1
        last_color = max(last_counts, key=last_counts.get)
        return last_color
    else:
        return "unknown"

# The MOST important funtion: continuously polls the color sensor, and takes the mean of every 10 polls
# This function has shown through testing to be very precise
def get_mean_color(color_sensor):
    color = closest_color(tuple(color_sensor.get_rgb()))
    #print(color)
    mean = mean_color(color)
    print("mean: "+mean)
    return mean