import audiogen
import datetime
import logging
from os import system, remove
import RPi.GPIO as GPIO
import time

import afsk.afsk
from afsk.ax25 import UI
from config import *


class GPS_Data:
    def __init__(self, h=None, t=None, s=None, current_datetime=None):

        self.h = h
        self.t = t
        self.s = s
        self.current_datetime = current_datetime

    def __str__(self):
        return "{},{},{}  {}".format(
            self.h,
            self.t,
            self.s,
            self.current_datetime,
        )


# GPS base class
# Override the setup and loop methods to create your own GPS readers/parsers
class Base_GPS:
    # Set this to a scheduler class so we can track when messages are sent
    scheduler = None

    gps_led_pin = None

    def setup(self):
        pass



    def loop(self):
        while(True):
            # Convert ISO 8601 date to a datetime object
            # 2018-03-06T02:43:10.000Z'
            self.gps_data.current_datetime = datetime.now()

            # Initialize the clock as this is the first valid timestamp we
            # have from the GPS data
            if self.start_datetime is None:
                self.start_datetime = self.gps_data.current_datetime

            if self.scheduler_ready():
                logging.info("Sending packet")
                self.send_packet()

    # shutdown method for cleaning up files, closing sockets, etc.
    def shutdown(self):
        pass

    # Initialize the class with empty GPS data and run the setup method
    # to pre-configure our GPS acquiring, assuming our method requires it.
    def __init__(self):
        self.start_datetime = None
        self.gps_data = GPS_Data()

        self.setup()

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

        info = "/{:%H%M%S}h{}{}{}{}{}{}{:03d}/{:03d}/A{:06d} {}".format(
            self.gps_data.current_datetime,  # datetime object
            APRS_SYMBOL1,  # Symbol lookup table, see config
            self.gps_data.h,
            self.gps_data.t,
            APRS_SYMBOL2,  # Symbol lookup table, see config
            self.gps_data.s,
            APRS_COMMENT,  # Set comment text in config
        )

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
        # audiogen.sampler.play(audio, blocking=True)

        system("play -q /tmp/output.wav")
        # remove("/tmp/output.wav")

        # Disable radio transmit
        GPIO.output(RADIO_TX_PIN, GPIO.LOW)

        # Signal to the scheduler that we sent a packet
        self.scheduler.sent(self.gps_data)

