from utils.brick import BP, TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
import time, math
from collections import deque

leftmotor = Motor("A")
rightmotor = Motor("D")
blue_color_sensor = EV3ColorSensor(3)
red_color_sensor = EV3ColorSensor(2)
sensor = TouchSensor(1)
sleepsensor = TouchSensor(4)


wait_ready_sensors(True)
print("Done waiting.")

def emergency_stop():
    #if this function is called that means touch sensor 3 was pressed
    #we stop everything, reset the brick pi and print the emergency stop message, and exit the program
        print('Emergency stop triggered')
        BP.reset_all()
        exit()

colors = {
    "black": {"mean": [0, 0, 0], "cov": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
    "white": {"mean": [300, 300, 200], "cov": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
    "red": {"mean": [250, 30, 30], "cov": [[100, 0, 0], [0, 100, 0], [0, 0, 100]]},
    "green": {"mean": [20, 100, 30], "cov": [[100, 0, 0], [0, 100, 0], [0, 0, 100]]},
    "blue": {"mean": [20, 30, 45], "cov": [[100, 0, 0], [0, 100, 0], [0, 0, 100]]},
    "yellow": {"mean": [300, 200, 20], "cov": [[100, 0, 0], [0, 100, 0], [0, 0, 100]]},
    #"orange": {"mean": [250, 60, 40], "cov": [[100, 0, 0], [0, 100, 0], [0, 0, 100]]},
    "purple": {"mean": [70, 50, 70], "cov": [[100, 0, 0], [0, 100, 0], [0, 0, 100]]},
    "map_white": {"mean": [300, 260, 170]},
    "map_tape": {"mean": [190, 170, 100]},
    "map_blue": {"mean": [37,60,60]},
    "map_blue_plus_tape": {"mean": [45,50,52]},
    "map_red": {"mean": [245,38,18]},
    "map_red_plus_tape": {"mean": [250,50,30]},
    "map_green": {"mean": [37,100,20]},
    "map_green_plus_tape": {"mean": [50,120,30]},
    #"red_white_boundary": {"mean": [255,100,75]},
    #"blue_white_boundary": {"mean": [280,255,160]},
    "pink": {"mean": [255, 192, 203], "cov": [[100, 0, 0], [0, 100, 0], [0, 0, 100]]},
}

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape"]
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
    static_color = closest_color(tuple(blue_color_sensor.get_rgb()))
    #print(color)
    mean_blue = mean_color(static_color)
    print("mean left: "+mean_blue)
    return mean_blue

def get_red_sensor():
    mobile_color = closest_color(tuple(red_color_sensor.get_rgb()))
    #print(color)
    mean_red = mean_color(mobile_color)
    print("mean right: "+mean_red)
    return mean_red

def follow_path():
    try:
        blue_path = get_blue_sensor()
        red_path = get_red_sensor()
        
        #last = get_last_30(blue_path)
        #print("last 30 mean: "+last)

        #print(color_sensor.get_rgb())

        if blue_path == "yellow" or red_path == "yellow":
            leftmotor.set_power(12)
            rightmotor.set_power(12)
        elif (blue_path in mapblue) and (red_path in mapred):
            leftmotor.set_power(12)
            rightmotor.set_power(12)
        elif (blue_path in mapblue) and (red_path not in mapred):
            leftmotor.set_power(12)
            rightmotor.set_power(12)    
        elif blue_path == "blue" or blue_path == "map_blue" or blue_path == "map_blue_plus_tape": 
            leftmotor.set_power(30)
            rightmotor.set_power(8)

        else:
            #print("No movement")
            leftmotor.set_power(12)
            rightmotor.set_power(12)
    
    except BaseException as error:
        print(error)


        
time.sleep(4)
try:
    while not sensor.is_pressed():
        if sleepsensor.is_pressed():
            print("sleep")
            time.sleep(3)
        follow_path()
        #print(color_sensor.get_rgb())
    emergency_stop()
except BaseException as error:
    print(error)
    exit()

