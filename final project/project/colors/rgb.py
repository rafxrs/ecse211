from utils.brick import TouchSensor, EV3ColorSensor, wait_ready_sensors
import time, math
from utils.emergency_stop import ES

def get_rgb():
    color_sensor = EV3ColorSensor(2)
    sensor = TouchSensor(1)
    wait_ready_sensors(True)
    print("Done waiting.")
    time.sleep(2)
        
    try:
        while not sensor.is_pressed():
            print(color_sensor.get_rgb())
        ES.emergency_stop()
    except BaseException as error:
        print(error)
        exit()
    
# Define the function to normalize RGB values
def normalize_rgb(r, g, b):
    denominator = math.sqrt(r**2+g**2+b**2)
    if denominator == 0:
        return 0,0,0
    normalized_r = r / math.sqrt(r**2 + g**2 + b**2)
    normalized_g = g / math.sqrt(r**2 + g**2 + b**2)
    normalized_b = b / math.sqrt(r**2 + g**2 + b**2)
    return normalized_r, normalized_g, normalized_b
    
