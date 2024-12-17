import ntptime
import machine
import time
from .logger import Logger

class Time:
    _rtc: machine.RTC = None
    _time_offset: int
    _days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, time_offset_hours: int = 0) -> None:
        self._time_offset = time_offset_hours


    def _adjust_time(self, offset: int):
        rtc_time = self._rtc.datetime()
        print("Before", rtc_time)
        (year, month, day, weekday, hours, minutes, seconds, subseconds)= rtc_time

        # Convert RTC datetime to a timestamp (assuming RTC is in UTC)
        try:
            current_timestamp = time.mktime((year, month, day, hours, minutes, seconds, 0, 0))
            print(f"RTC timestamp: {current_timestamp}")
        except OverflowError as e:
            Logger.print(f"Error converting to timestamp: {e}")
            return

        # Apply the offset in seconds
        adjusted_timestamp = current_timestamp + offset * 3600
        print(f"Adjusted timestamp: {adjusted_timestamp}")

        # Convert the adjusted timestamp back to a localtime tuple
        try:
            adjusted_time = time.localtime(adjusted_timestamp)
            print(f"Adjusted time tuple: {adjusted_time}")
        except OverflowError as e:
            Logger.print(f"Error converting back to time tuple: {e}")
            return

        # Update RTC with adjusted time
        year, month, day, hours, minutes, seconds, weekday, subseconds = adjusted_time
        self._rtc.datetime((year, month, day, weekday, hours, minutes, seconds, subseconds))
        print("After", self._rtc.datetime())


    def sync(self):
        for _ in range(3):  # Retry up to 3 times
            try:
                ntptime.settime()
                self._rtc = machine.RTC()
                self._adjust_time(self._time_offset)
                return
            except OSError as e:
                Logger.print(f"NTP synchronization failed: {e}")
                time.sleep(5)
    # year, month, day, weekday, hours, minutes, seconds, subseconds
    def current_time(self):
        if self._rtc is None:
            Logger.print("Syncing time...")
            self.sync()
        return self._rtc.datetime()
    
    def current_hour(self):
        try:
            return self._rtc.datetime()[4]
        except AttributeError:
            Logger.print("Have you called sync before?")
            return None

    def current_timestamp_seconds(self) -> int:
        if self._rtc is None:
            Logger.print("RTC is not initialized. Call sync() first.")
            return 0

        date = self._rtc.datetime()
        year, month, day, weekday, hours, minutes, seconds, _ = date  # Ignore subseconds
        try:
            # Provide a valid tuple for mktime: (year, month, day, hours, minutes, seconds, weekday, yearday)
            seconds_since_epoch = time.mktime((year, month, day, hours, minutes, seconds, weekday, 0))
            return seconds_since_epoch
        except OverflowError as e:
            Logger.print
            return 0