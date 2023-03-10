from utils.brick import BP, TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
import time
from utils.emergency_stop import ES

color_sensor = EV3ColorSensor(3)
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