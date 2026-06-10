from kivy.logger import Logger
from .horn import Horn

class Race:
    def __init__(self):
        self._horn = Horn()
        Logger.debug("Race created")

    def start(self):
        self._horn.sound()
        Logger.debug("Race started")
    
    def stop(self):
        self._horn.sound()
        Logger.debug("Race stopped")
