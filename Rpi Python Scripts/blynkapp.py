import blynklib

from sense_hat import SenseHat

from gpiozero import MotionSensor
from time import sleep

# IFTTT webhook requests
import requests

sense = SenseHat()

# variable for the Motion Sensor connected to pin 17
pir = MotionSensor(17)

sense.clear()
sense.low_light = True

BLYNK_AUTH = '39GdI0DcuPiMwH-zf0vlmojtrdZqB0Ae'

blynk = blynklib.Blynk(BLYNK_AUTH)

# set up colour varuables for the LED matrix
g = [0,50,0] # green
r = [50,0,0] # red

# register handler for virtual pin V1(temperature) reading
@blynk.handle_event('read V1')
def read_virtual_pin_handler(pin):
    temp=round(sense.get_temperature(),2)
    print('V1 Read: ' + str(temp))     # print temp to console
    blynk.virtual_write(1, temp)
    
    # lower temp threshold reached, activate the smart socket to run the heater
    if temp < 22.5:
        requests.post("https://maker.ifttt.com/trigger/temp_too_low/with/key/7Gh5PG6SmrOXa87SOAlZr")
        blynk.virtual_write(2,255)
    
    # upper temp threshold reached, deactivate the heater
    if temp > 23:
        requests.post("https://maker.ifttt.com/trigger/temp_too_high/with/key/7Gh5PG6SmrOXa87SOAlZr")
        blynk.virtual_write(2,0)

# variables for controlling the notification upon motion detection
foo = 0
bar = 1

while True:
    blynk.run()

    # set foo to match the PIR's activity
    if pir.value == 0:
        foo = 0
        # show that the camra is off via the LED matrix
        sense.load_image("images/red_x.bmp")
    else:
        foo = 1
        # show the camera is streaming via the LED matrix
        sense.load_image("images/green_tick.bmp")

    # motion detected, send a notification to the blynk app, and update bar
    if foo == 1 & bar == 1:
        print("Motion Detected!")
        blynk.notify("Motion Detected!")
        bar = 2
    
    # reset foo and bar's relative initial states
    if foo == 0:
       bar = 1