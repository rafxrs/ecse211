# Simple file to test a single motor
from utils.brick import BP, TouchSensor, Motor, wait_ready_sensors, reset_brick
import time
actionsensor = TouchSensor(4)
stopsensor = TouchSensor(1)
motor = Motor("B")
POWER_LIMIT = 20       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second
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
    # Encoder keeps a record of degrees turned
    motor.reset_encoder()                      # Reset encoder to 0 value
    motor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    motor.set_power(0)
    while not stopsensor.is_pressed():
        if actionsensor.is_pressed():
            motor.set_power(10)
    emergency_stop()
except BaseException as error:
    print(error)
    exit()