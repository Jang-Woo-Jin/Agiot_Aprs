from config import SCHEDULER_TIME_INTERVAL

class APRSScheduler:
    # The GPS data from the last time we sent out a packet.
    last_packet_gps_data = None

    def ready(self, gps_data=None, start_datetime=None):
        # Overload this function to determine if we're ready to send a packet.
        # True if it's time to send one
        # False if the time is not quite right
        #
        # Arguments are
        # - GPS Data class populated with the current GPS fix and time
        # - The first datetime we received from the position source to track
        #   how long this script has been running.
        pass


    def sent(self, gps_data):
        # When a packet is sent, keep a backup of the previous packet for
        # determining when to send the next one.
        self.last_packet_gps_data = gps_data


class TimerScheduler(APRSScheduler):
    """
    Very simple scheduler. Send a message every SCHEDULER_TIME_INTERVAL seconds.
    Returns True if we're ready to send our message.
    """

    def ready(self, gps_data, start_datetime):

        # Probably should log this one, could get stuck here I guess
        if start_datetime is None:
            return False

        # First packet of the loop, always just send it
        if not self.last_packet_gps_data:
            return True


        if (gps_data.current_datetime - self.last_packet_gps_data.current_datetime).total_seconds() >= SCHEDULER_TIME_INTERVAL:
            return True

        return False