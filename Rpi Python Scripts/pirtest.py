#!/usr/bin/python3

from gpiozero import MotionSensor
from time import sleep
from signal import pause

pir = MotionSensor(17)
while True:
    pir.wait_for_motion()
    print("Who's there?")
    sleep(1)