from utils.brick import BP, TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
import time

leftmotor = Motor("A")
rightmotor = Motor("B")
sensor = TouchSensor(1)

wait_ready_sensors(True)
print("Done waiting.")

def emergency_stop():
    #if this function is called that means touch sensor 3 was pressed
    #we stop everything, reset the brick pi and print the emergency stop message, and exit the program
        print('Emergency stop triggered')
        BP.reset_all()
        exit()

try:
    while not sensor.is_pressed():
        leftmotor.set_power(40)
        rightmotor.set_power(40)
    emergency_stop()
except BaseException as error:
    print(error)
    exit()



