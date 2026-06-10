from datetime import datetime
import uuid
from kivy.logger import Logger
from kivy.clock import Clock

from .horn import Horn

INTERVALS = [0, 1, 4, 5]


class Race:
    def __init__(self):
        self._countdownDateTime = None
        self._startDateTime = None
        self._finishDateTime = None
        self._horn = Horn()
        self._intervals = []
        self._id = uuid.uuid4()
        self._state = "IDLE"
        self._debug("Created")

    def getState(self):
        return self._state

    def isRunning(self):
        return self._state != "IDLE"

    def getElapsedTime(self):
        if not self.isRunning():
            return None
        elapsed_time = (
            self._finishDateTime or datetime.now()
        ) - self._countdownDateTime
        return elapsed_time

    def interval(self, dt):
        self._debug("Interval at " + str(dt))
        self._horn.sound()

    def countdown(self):
        self._debug("Beginning countdown...")
        for i, interval in enumerate(INTERVALS):
            seconds = interval * 60
            if i < len(INTERVALS) - 1:
                timer = Clock.schedule_once(self.interval, seconds)
            else:
                timer = Clock.schedule_once(self.start, seconds)
            self._intervals.append(timer)
            self._debug("Scheduled interval at " + str(seconds) + " seconds")
        self._countdownDateTime = datetime.now()
        self._state = "COUNTDOWN"

    def start(self, dt):
        self.interval(dt)
        self._startDateTime = datetime.now()
        self._state = "RUNNING"
        self._debug("Started at " + str(self._startDateTime))

    def stop(self):
        for timer in self._intervals:
            Clock.unschedule(timer)
        self._finishDateTime = datetime.now()
        self._horn.sound()
        self._state = "FINISHED"
        self._debug("Stopped at " + str(self._finishDateTime))

    def _debug(self, message):
        Logger.debug("Race: " + str(self._id) + ": " + message)
