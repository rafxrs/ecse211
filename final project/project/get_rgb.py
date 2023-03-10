from utils.brick import BP, TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
import time, math
from collections import deque

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

time.sleep(2)
try:
    while not sensor.is_pressed():
        print(color_sensor.get_rgb())
    emergency_stop()
except BaseException as error:
    print(error)
    exit()