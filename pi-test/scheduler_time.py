from config import SCHEDULER_TIME_INTERVAL

class APRSScheduler:
    # The GPS data from the last time we sent out a packet.
    last_packet_gps_data = None

    def ready(self, gps_data=None, start_datetime=None):
        pass


    def sent(self, gps_data):
        self.last_packet_gps_data = gps_data


class TimerScheduler(APRSScheduler):
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