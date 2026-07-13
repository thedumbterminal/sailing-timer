from datetime import datetime
from kivy.clock import Clock

from .countdown import Countdown
from .race_events import RaceEvents
from .horn import Horn
from .log import Log


class Race:
    def __init__(self):
        self._start_datetime = None
        self._finish_datetime = None
        self._log = Log(self)
        self._horn = Horn()
        self._countdowns = []
        self._intervals = []
        self._state = ""
        self._splits = []

        self._events = RaceEvents()
        self._set_state("IDLE")
        self._log.debug("Created")

    def _set_state(self, new_state):
        old_state = self._state
        self._state = new_state
        self._log.debug("State changed from " + old_state + " to " + new_state)
        self._events.dispatch("on_state_change", old_state, new_state)

    def get_events(self):
        return self._events

    def get_state(self):
        return self._state

    def is_running(self):
        return self.get_state() == "STARTED"

    def is_counting_down(self):
        return self.get_state() == "COUNTDOWN"

    def get_elapsed_time(self):
        if self.get_state() == "IDLE":
            return None
        elapsed_time = (self._finish_datetime or datetime.now()) - self._start_datetime
        return elapsed_time

    def countdown(self):
        self._start_datetime = datetime.now()
        self._log.debug("Beginning countdown")
        countdown = Countdown(callback=self.start)
        self._countdowns.append(countdown)
        countdown.begin()
        self._set_state("COUNTDOWN")

    def start(self):
        self._set_state("STARTED")
        self._log.debug("Started")

    def stop(self):
        for timer in self._intervals:
            Clock.unschedule(timer)
        self._finish_datetime = datetime.now()
        self._set_state("FINISHED")
        self._log.debug("Finished")
        self._horn.sound()

    def add_split(self):
        now = datetime.now()
        self._splits.append(now)
        self._log.debug("Split added")
        self._horn.sound()

    def get_splits(self):
        return self._splits

    def get_countdowns(self):
        return self._countdowns
