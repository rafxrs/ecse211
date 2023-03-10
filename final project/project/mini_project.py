#import all the libraries we will be using
#we need sound for the notes we will play
#we need to import time and sleep to tell the sensors to sleep and define the duration of the notes
#we need to import a few brick pi libraries
from utils import sound
from utils.brick import BP, TouchSensor, EV3ColorSensor, Motor, wait_ready_sensors, reset_brick
from time import sleep
from utils.sound import Sound
import time

#Defining the four different notes the flute will play
tone1 = Sound(duration=1.0, volume=90, pitch="E4")
tone2 = Sound(duration=1.0, volume=90, pitch="C4")
tone3 = Sound(duration=1.0, volume=80, pitch="G4")
tone4 = Sound(duration=1.0, volume=90, pitch="F4")

print("Program start.\nWaiting for sensors to turn on...")

#Initializing all sensors
#Port 1 for the touch sensor that will start the drumming mechanism
#Port 3 for the touch sensor that will trigger the emergency stop
#Port 2 for the color sensor
#Port D for the motor that implements the drumming mechanism
TOUCH_SENSOR1 = TouchSensor(1)
TOUCH_SENSOR3 = TouchSensor(3)
COLOR_SENSOR = EV3ColorSensor(2)
Motor = Motor("D")

wait_ready_sensors(True)
print("Done waiting.")

#define a function that plays a single note from a specific sound object
def play_sound(sound):
    #Play a single note.
    sound.play()
    sound.wait_done()

#this function gets the name of the color that the color sensor sees, and depending on the color, plays a specific note, or plays no note
def flute():
    try: 
        color_name = COLOR_SENSOR.get_color_name();
        print(color_name) #this is not needed, it is just so that we can see what our color sensor is seeing

        if color_name == "Red": #red is for tone1
            play_sound(tone1)
        elif color_name == "Green": #green is for tone2
            play_sound(tone2)
        elif color_name == "Blue": #blue is for tone3
            play_sound(tone3)
        elif color_name == "Yellow": #yellow is for tone4
            play_sound(tone4)
        elif color_name == 'Black' or 'White' or 'Unknown': #these are colors that happen sometimes when there is no cube in front
            print("No sound playing (black, white, unknown)")
        else:
            print("No sound playing") 
    except BaseException as error: #print the error message if there is an error
        print(error)

def emergency_stop():
    #if this function is called that means touch sensor 3 was pressed
    #we stop everything, reset the brick pi and print the emergency stop message, and exit the program
        print('Emergency stop triggered')
        BP.reset_all()
        exit()

print("marching band function reached")
try:
    drum_started = False #this variable is created so that we don't try to start the drum twice
    while True:
        while not TOUCH_SENSOR3.is_pressed(): #check for eemergency stop
            drum = TOUCH_SENSOR1.is_pressed() #check for drum sensor
            if drum and not drum_started: #if drum sensor trigerred & the drum wasn't previously started, start drum
                print("Drum started")
                Motor.set_power(30)
                drum_started = True #so we don't start the drum twice
            time.sleep(0.5) #sleep 0.5 s between two notes
            flute() #get the color the sensor is seeing and play corresponding note
            print("No emergency stop") #emergency stop wasn't triggered, keep playing (this is not needed, it is more to see what the program is doing while it runs)
        emergency_stop() #only reached if touch sensor 3 is pressed --> we call emergency_stop() when we see sensor 3 was triggered
except BaseException as error:
    # On exception or error, print error code
    print(error)
    exit()

