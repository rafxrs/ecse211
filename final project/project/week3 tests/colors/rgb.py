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
    
    
