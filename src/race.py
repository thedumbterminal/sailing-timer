from datetime import datetime
import uuid
from kivy.logger import Logger
from kivy.clock import Clock

from .race_events import RaceEvents
from .horn import Horn

# Production intervals
# INTERVALS = [0, 1, 4, 5]

# Testing intervals
INTERVALS = [0, 0.5]


class Race:
    def __init__(self):
        self._countdown_datetime = None
        self._start_datetime = None
        self._finish_datetime = None
        self._horn = Horn()
        self._intervals = []
        self._id = uuid.uuid4()
        self._state = ""
        self._splits = []

        self._events = RaceEvents()
        self._set_state("IDLE")
        self._debug("Created")

    def _set_state(self, new_state):
        old_state = self._state
        self._state = new_state
        self._debug("State changed from " + old_state + " to " + new_state)
        self._events.dispatch("on_state_change", old_state, new_state)

    def _debug(self, message):
        Logger.debug("Race: " + str(self._id) + ": " + message)

    def get_events(self):
        return self._events

    def get_state(self):
        return self._state

    def is_running(self):
        return self.get_state() == "RUNNING"

    def get_elapsed_time(self):
        if self.get_state() == "IDLE":
            return None
        elapsed_time = (
            self._finish_datetime or datetime.now()
        ) - self._countdown_datetime
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
        self._countdown_datetime = datetime.now()
        self._set_state("COUNTDOWN")

    def start(self, dt):
        self.interval(dt)
        self._start_datetime = datetime.now()
        self._debug("Started at " + str(self._start_datetime))
        self._set_state("RUNNING")

    def stop(self):
        for timer in self._intervals:
            Clock.unschedule(timer)
        self._finish_datetime = datetime.now()
        self._horn.sound()
        self._debug("Stopped at " + str(self._finish_datetime))
        self._set_state("FINISHED")

    def add_split(self):
        now = datetime.now()
        self._splits.append(now)
        self._horn.sound()
        self._debug("Split added at " + str(now))

    def get_splits(self):
        return self._splits
