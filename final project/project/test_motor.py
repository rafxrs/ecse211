from utils.brick import BP, TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
import time, math

sleepsensor = TouchSensor(4)
sensor = TouchSensor(1)
pistonmotor = Motor("C")

#This is a testing file to test a single motor

POWER_LIMIT = 20       # Power limit = 
SPEED_LIMIT = 360      # Speed limit = 720 deg per sec (dps)

wait_ready_sensors(True)
print("Done waiting.")

def emergency_stop():
    #if this function is called that means touch sensor 3 was pressed
    #we stop everything, reset the brick pi and print the emergency stop message, and exit the program
        print('Emergency stop triggered')
        BP.reset_all()
        exit()

time.sleep(4)
try:
    # Encoder keeps a record of degrees turned
    pistonmotor.reset_encoder()                      # Reset encoder to 0 value
    pistonmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
    pistonmotor.set_power(0)

    while not sensor.is_pressed():
        if sleepsensor.is_pressed():
            print("sleep")
            time.sleep(3)
        print("Motor Position Control Test")
        pistonmotor.set_position(360) 
    emergency_stop()
except BaseException as error:
    print(error)
    exit()