#!/usr/bin/env python

import logging
from os import system
import RPi.GPIO as GPIO
import sys
import time

import audiogen
import datetime
from os import system, remove
import RPi.GPIO as GPIO

import afsk.afsk
from afsk.ax25 import UI
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# If you create additional scheduler and GPS classes, specify them
# here with additional logic.

if SCHEDULER_CLASS == "time":
    from scheduler_time import TimerScheduler as Scheduler
elif SCHEDULER_CLASS == "smart":
    from scheduler_smart import SmartScheduler as Scheduler

"""
class GPS_Data:
    def __init__(self, fix=False, latitude=None, latitude_direction=None,
        longitude=None, longitude_direction=None, altitude=None, 
        course=None, speed=None, current_datetime=None):

        self.fix = fix
        self.latitude = latitude
        self.latitude_direction = latitude_direction
        self.longitude = longitude
        self.longitude_direction = longitude_direction
        self.altitude = altitude
        self.course = course
        self.speed = speed
        self.current_datetime = current_datetime

    def __str__(self):
        if self.fix:
            fix = "3D FIX"
        else:
            fix = "FIX"
        return "{} {},{}  {} ft  {} deg  {} kts {}".format(
            fix,
            self.latitude,
            self.longitude,
            self.altitude,
            self.course,
            self.speed,
            self.current_datetime,
        )
"""
# GPS base class
# Override the setup and loop methods to create your own GPS readers/parsers
class Base_GPS:
    # Set this to a scheduler class so we can track when messages are sent
    scheduler = None


    # Initialize the class with empty GPS data and run the setup method
    # to pre-configure our GPS acquiring, assuming our method requires it.
    def __init__(self):
        self.start_datetime = None
        self.gps_data = "test" #GPS_DATA()

    # Check if our scheduler class determines if we are ready to send a packet.
    # Supply it with the current GPS data and the begining time.
    def scheduler_ready(self):
        ready = self.scheduler.ready(
            gps_data=self.gps_data,
            start_datetime=self.start_datetime,
        )

        if ready:
            logging.info("Scheduler says its time to send a packet")
        else:
            logging.info("Scheduler not ready")

        return ready


    # Send out a formatted APRS packet using the current GPS data
    def send_packet(self):
        # Format callsign and SSID
        # ABC123-4 with a SSID and ASB123 without one
        if CALLSIGN_SSID == "" or CALLSIGN_SSID == 0:
            callsign = CALLSIGN
        else:
            callsign = "{}-{}".format(CALLSIGN, CALLSIGN_SSID)

        
        # Same thing for the destination and SSID. SSID is not typically used
        # for destinations in the APRS world.
        if DESTINATION_SSID == "" or DESTINATION_SSID == 0:
            destination = DESTINATION
        else:
            destination = "{}-{}".format(DESTINATION, DESTINATION_SSID)


        # Format digipeater paths. These are split by commas and properly encoded
        # in a bytestream, as they are a key ingredient in generating the CRC bits.
        digipeaters = DIGIPEATING_PATH.split(b',')


        # Format APRS info string
        # APRS Info string goes something like this:
        # /235619h4304.95N/08912.63W>000/003/A=000859 comment
	"""
        info = "/{:%H%M%S}h{}{}{}{}{}{}{:03d}/{:03d}/A{:06d} {}".format(
            self.gps_data.current_datetime,         # datetime object
            self.gps_data.latitude,                 # 04304.95
            self.gps_data.latitude_direction,       # N/S
            APRS_SYMBOL1,                           # Symbol lookup table, see config
            self.gps_data.longitude,                # 08912.63
            self.gps_data.longitude_direction,      # E/W
            APRS_SYMBOL2,                           # Symbol lookup table, see config
            self.gps_data.course,                   # Magnetic heading
            self.gps_data.speed,                    # Speed in knots
            self.gps_data.altitude,                 # Altitude to meters
            APRS_COMMENT,                           # Set comment text in config
        )
	"""
	info = self.gps_data        
	logging.info("{}>{},{}:{}".format(
            callsign,
            destination,
            DIGIPEATING_PATH,
            info,
        ))


        # Create packet. This formats the headers with CRC checksums and all that
        # stuff that we're grateful we didn't have to figure out ourselves.
        packet = UI(
                source=callsign,
                destination=destination,
                digipeaters=digipeaters,
                info=info,
        )
        audio = afsk.encode(packet.unparse())


        # Sometimes for debugging saving the generated .wav is helpful.
        # Make sure this location is in a ramdisk!
        with open("/tmp/output.wav", "w") as f:
            audiogen.sampler.write_wav(f, audio)
            

        # Enable radio transmit push-to-talk pin by driving it high.
        GPIO.output(RADIO_TX_PIN, GPIO.HIGH)

        # Wait for the PTT to activate and the radio to actually be transmitting.
        # Also gives iGates and clients a chance to listen for the actual message.
        # However... we don't want to set this too long or we just consume valuable
        # airtime.
        time.sleep(RADIO_TX_DELAY / 1000.0)

        # Play the audio sample out the PWM pin
        # For some reason this results in garbled audio
        #audiogen.sampler.play(audio, blocking=True)

        #system("play -q /tmp/output.wav")
        #remove("/tmp/output.wav")

        # Disable radio transmit
        GPIO.output(RADIO_TX_PIN, GPIO.LOW)


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

    ## need to send	
    test = Base_GPS()
    test.send_packet()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        # Turn off the lights
        GPIO.output(ALL_OUTPUT_PINS, GPIO.LOW)
        GPIO.cleanup()

        # Close the door
        sys.exit(0)

