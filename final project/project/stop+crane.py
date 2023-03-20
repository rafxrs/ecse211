from utils.brick import TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors
from utils.emergency_stop import ES
from collections import deque
from colors import color_info
import time, math


leftmotor = Motor("D")
rightmotor = Motor("A")
cranemotor = Motor("B")
static_color_sensor = EV3ColorSensor(3)
mobile_color_sensor = EV3ColorSensor(2)
sensor = TouchSensor(1)
actionsensor = TouchSensor(4)

wait_ready_sensors(True)
print("Done waiting.")

colors_dict = color_info.get_cd()

#This is for the crane
POWER_LIMIT = 20       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]


# Define the threshold for color distance
static_color_threshold = 50
mobile_color_threshold = 75

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
def static_closest_color(rgb_values):
    min_distance = float('inf')
    closest_color = None
    for color_name, color_values in colors_dict.items():
        distance = color_distance(rgb_values, color_values["mean"])
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    if min_distance < static_color_threshold:
        return closest_color
    else:
        return None
    
# Define the function to get the closest color
def mobile_closest_color(rgb_values):
    min_distance = float('inf')
    closest_color = None
    for color_name, color_values in colors_dict.items():
        distance = color_distance(rgb_values, color_values["mean"])
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    if min_distance < mobile_color_threshold:
        return closest_color
    else:
        return None

static_color_polls = deque(maxlen=10)

def static_mean_color(color_name):
    
    static_color_polls.append(color_name)
    #print(len(color_polls))
    if len(static_color_polls) == 10:
        color_counts= {}
        for color in static_color_polls:
            if color in color_counts:
                color_counts[color]+=1
            else:
                color_counts[color]=1
        mode_color = max(color_counts, key=color_counts.get)
        return mode_color
    else:
        return "unknown"

mobile_color_polls = deque(maxlen=10)

def mobile_mean_color(color_name):
    
    mobile_color_polls.append(color_name)
    #print(len(color_polls))
    if len(mobile_color_polls) == 10:
        color_counts= {}
        for color in mobile_color_polls:
            if color in color_counts:
                color_counts[color]+=1
            else:
                color_counts[color]=1
        mode_color = max(color_counts, key=color_counts.get)
        if mode_color in mapred: return "red"
        elif mode_color in mapblue: return "blue"
        elif mode_color in mapgreen: return "green"
        return mode_color
    else:
        return "unknown"
    
def get_static_sensor():
    color = static_closest_color(tuple(static_color_sensor.get_rgb()))
    #print(color)
    mean = static_mean_color(color)
    #print("mean: "+mean)
    return mean

def get_mobile_sensor():
    mobile_color = mobile_closest_color(tuple(mobile_color_sensor.get_rgb()))
    #print(color)
    mean_red = mobile_mean_color(mobile_color)
    #print("mean right: "+mean_red)
    return mean_red

last_20 = deque(maxlen=20)

def get_last_20(mean):
    last_20.append(mean)
    #print(len(color_polls))
    if len(last_20) == 20:
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

delivery_colors= []
def follow_path():
    try:
        cranemotor.reset_encoder()                      # Reset encoder to 0 value
        cranemotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits

        path = get_static_sensor()
        delivery_color = get_mobile_sensor()
        last = get_last_20(delivery_color)

        print(mobile_color_sensor.get_rgb())
        
        if path in mapred:
            leftmotor.set_power(8)
            rightmotor.set_power(35)
        elif path in mapblue: 
            leftmotor.set_power(35)
            rightmotor.set_power(8)
        elif (path in mapgreen):
            leftmotor.set_power(0)
            rightmotor.set_power(0)
            #adjust_robot()
            
            #cranemotor.set_position_relative(90)
            for i in range (5):
                print(mobile_color_sensor.get_rgb())
                time.sleep(1)
            #cranemotor.set_position_relative(-90)
            
            print("color: "+ last)
            delivery_colors.append(last)

            while path in mapgreen:
                path = get_static_sensor()
                leftmotor.set_power(18)
                rightmotor.set_power(18)
        else:
            leftmotor.set_power(18)
            rightmotor.set_power(18)
    
    except BaseException as error:
        print(error)


        
time.sleep(4)
try:
    while not sensor.is_pressed():
        follow_path()
    print(delivery_colors)
    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()

