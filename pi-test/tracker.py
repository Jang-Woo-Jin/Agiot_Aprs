#!/usr/bin/env python

import logging
from os import system
import RPi.GPIO as GPIO
import sys
import time

from config import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# If you create additional scheduler and GPS classes, specify them
# here with additional logic.

from scheduler_time import TimerScheduler as Scheduler
from gps_gpsd import Base_GPS as GPS


# Create the GPS class to read GPS data, assign a scheduler to decide when
# we want to send packets and assign the GPS LED pin number.
gps = GPS()
gps.scheduler = Scheduler()
gps.gps_led_pin = YELLOW_LED_PIN


# TODO
# test GPS disconnecting
# test GPSD dying
# fstab -> tmpdisk
# tune amount of tx delay (doesn't seem to make a difference)
# test set volume (amixer set PCM -- 400)
# shut off NTP and other things on this image
# ensure that hopping to the next day works with the weird clock
# lockfile, kill old socket if found
# use altitude gain/loss in smart algo
# first packet has incorrect date


def main():
    # Configure our LED and TX pins
    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ALL_OUTPUT_PINS, GPIO.OUT, initial=GPIO.LOW)

    # Python GPIO library does not support setting the special modes
    # of the pins, so we have to call an external command for that.
    # This enables us to pipe the audio out of the PWM pin directly to the
    # radio.
    system("raspi-gpio set {} a5".format(RADIO_PWM_PIN))

    # One of the projects that we borrowed code from recommended setting
    # the volume level. 
    system("amixer set PCM -- 400")

    # Loop through the GPS data as we receive it.
    gps.loop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("keyboard interrupt")
        # Turn off the lights
        GPIO.output(ALL_OUTPUT_PINS, GPIO.LOW)
        GPIO.cleanup()

        # Close files and socket connections
        gps.shutdown()
        
        # Close the door
        print("Exit!")
        sys.exit(0)
