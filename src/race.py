from datetime import datetime
from kivy.logger import Logger
from kivy.clock import Clock

from .countdown import Countdown
from .race_events import RaceEvents
from .horn import Horn


class Race:
    def __init__(self):
        self._start_datetime = None
        self._finish_datetime = None
        self._horn = Horn()
        self._countdown = Countdown(callback=self.start)
        self._intervals = []
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
        Logger.debug(type(self).__name__ + ": " + message)

    def get_events(self):
        return self._events

    def get_state(self):
        return self._state

    def is_running(self):
        return self.get_state() == "STARTED"

    def get_elapsed_time(self):
        if self.get_state() == "IDLE":
            return None
        elapsed_time = (self._finish_datetime or datetime.now()) - self._start_datetime
        return elapsed_time

    def countdown(self):
        self._start_datetime = datetime.now()
        self._debug("Beginning countdown at " + str(self._start_datetime))
        self._countdown.begin()
        self._set_state("COUNTDOWN")

    def start(self):
        self._set_state("STARTED")
        self._debug("Started at " + str(datetime.now()))

    def stop(self):
        for timer in self._intervals:
            Clock.unschedule(timer)
        self._finish_datetime = datetime.now()
        self._set_state("FINISHED")
        self._debug("Finished at " + str(self._finish_datetime))
        self._horn.sound()

    def add_split(self):
        now = datetime.now()
        self._splits.append(now)
        self._debug("Split added at " + str(now))
        self._horn.sound()

    def get_splits(self):
        return self._splits
