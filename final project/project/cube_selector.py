"""
Program for the sliding mechanism
"""

from utils.brick import Motor, TouchSensor, BP, wait_ready_sensors
from utils.emergency_stop import ES

#Initialize sensors
stopsensor = TouchSensor(1)
motor = Motor("C")

cube_positions = {
    "red": 0,
    "orange": 90,
    "yellow": 180,
    "green": 270,
    "blue": 360,
    "purple": 450
}
positions=[0, 90, 180, 270, 360, 450]

#Initialize sensors
wait_ready_sensors(True)
print("Done waiting")

# To move to a specific position (input angle)
def move_to_position(position):
    position = positions[position] 
    BP.set_motor_position(motor, position)

#Move to a specific cube position: works with color name
def move_to_cube_position(color_name):
    position = cube_positions[color_name] 
    BP.set_motor_position(motor, position)

#Puts moto to initial position
def reset_motor():
    BP.set_motor_position(motor, 0)

#Main function
try:
    while not stopsensor.is_pressed:
        #Comment out one of those lines depending on what you want to test
        position = int(input("What position should we move to?"))
        cube_position= input("What cube position shuld we move to?")

        #same here
        move_to_position(position)
        move_to_cube_position(cube_position)
        

    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()
