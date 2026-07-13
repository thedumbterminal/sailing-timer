import uuid
from dataclasses import dataclass
from datetime import datetime

from kivy.logger import Logger
from kivy.clock import Clock
from .horn import Horn

# Production intervals
# INTERVALS = [0, 1, 4, 5]

# Testing intervals
INTERVALS = [0, 0.5]


@dataclass
class Timing:
    time: datetime
    state: str


class Countdown:
    def __init__(self, callback):
        self._callback = callback
        self._state = "IDLE"
        self._id = uuid.uuid4()
        self._intervals = []
        self._timings = []
        self._horn = Horn()

    def _debug(self, message):
        Logger.debug(type(self).__name__ + ": " + str(self._id) + ": " + message)

    def _set_state(self, new_state):
        old_state = self._state
        self._state = new_state
        self._debug("Countdown: State changed from " + old_state + " to " + new_state)

    def _get_state(self):
        return self._state

    def _record_timing(self):
        t = Timing(time=datetime.now(), state=self._get_state())
        self._timings.append(t)

    def interval(self, dt):
        self._record_timing()
        self._debug("Interval at " + str(dt))
        self._horn.sound()

    def completed(self, dt):
        self._set_state("COMPLETED")
        self._record_timing()
        self._debug("Countdown finished at " + str(dt))
        self._callback()

    def begin(self):
        self._debug("Beginning countdown...")
        for i, interval in enumerate(INTERVALS):
            seconds = interval * 60
            if i < len(INTERVALS) - 1:
                timer = Clock.schedule_once(self.interval, seconds)
            else:
                timer = Clock.schedule_once(self.completed, seconds)
            self._intervals.append(timer)
            self._debug("Scheduled interval at " + str(seconds) + " seconds")
        self._set_state("COUNTDOWN")
        self._record_timing()
