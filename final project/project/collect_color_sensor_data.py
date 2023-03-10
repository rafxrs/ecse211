#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(2)
TOUCH_SENSOR = TouchSensor(1)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    "Collect color sensor data."
    try:
        file = open(COLOR_SENSOR_DATA_FILE,"w")
        while not TOUCH_SENSOR.is_pressed():
            pass
        print('Touch sensor pressed')
        print("Starting to collect data samples")
        numpresses =0 #number of times touch sensor was pressed
        while True:
            if TOUCH_SENSOR.is_pressed():
                numpresses+=1
                color = COLOR_SENSOR.get_value()
                
                if color is not None:
                    del color[3] #remove 4th item in list
                    color_string = str(color)
                    color_string = color_string.strip("[]") #get output formqt
                    print(color_string)
                    file.write(f"{color_string}\n") #write into csv file
                sleep(1)
                print(numpresses)
                if numpresses == 25: break #max amount of samples is x touch sensor presses
    except BaseException:
        pass
    finally:
        print("Done calculating color samples")
        file.close()
        reset_brick()
        exit()
        
        
if __name__ == "__main__":
    collect_color_sensor_data()
