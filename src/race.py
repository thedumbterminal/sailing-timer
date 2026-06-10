from datetime import datetime

from kivy.logger import Logger
from kivy.clock import Clock

from .horn import Horn

INTERVALS = [1, 4, 5]


class Race:
    def __init__(self):
        self._startDateTime = None
        self._finishDateTime = None
        self._horn = Horn()
        self._intervals = []
        Logger.debug("Race: Created")

    def interval(self, dt):
        Logger.debug("Race: Interval at " + str(dt))
        self._horn.sound()

    def start(self):
        self._startDateTime = datetime.now()
        self._horn.sound()
        for interval in INTERVALS:
            seconds = interval * 60
            timer = Clock.schedule_once(self.interval, seconds)
            self._intervals.append(timer)
            Logger.debug("Race: Scheduled interval at " + str(seconds) + " seconds")
        Logger.debug("Race: Started at " + str(self._startDateTime))

    def stop(self):
        self._finishDateTime = datetime.now()
        self._horn.sound()
        Logger.debug("Race: Stopped at " + str(self._finishDateTime))
