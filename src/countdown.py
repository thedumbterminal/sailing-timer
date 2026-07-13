import uuid
from dataclasses import dataclass
from datetime import datetime

from kivy.clock import Clock
from .horn import Horn
from .Log import Log

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
        self._log = Log(self)

    def _set_state(self, new_state):
        old_state = self._state
        self._state = new_state
        self._log.debug("Countdown: State changed from " + old_state + " to " + new_state)

    def _get_state(self):
        return self._state

    def _record_timing(self):
        t = Timing(time=datetime.now(), state=self._get_state())
        self._timings.append(t)

    def interval(self, dt):
        self._record_timing()
        self._log.debug("Interval at " + str(dt))
        self._horn.sound()

    def completed(self, dt):
        self._set_state("COMPLETED")
        self._record_timing()
        self._log.debug("Countdown finished at " + str(dt))
        self._callback()

    def begin(self):
        self._log.debug("Beginning countdown...")
        for i, interval in enumerate(INTERVALS):
            seconds = interval * 60
            if i < len(INTERVALS) - 1:
                timer = Clock.schedule_once(self.interval, seconds)
            else:
                timer = Clock.schedule_once(self.completed, seconds)
            self._intervals.append(timer)
            self._log.debug("Scheduled interval at " + str(seconds) + " seconds")
        self._set_state("COUNTDOWN")
        self._record_timing()
