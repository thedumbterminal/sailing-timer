from kivy.logger import Logger

class Horn:
    def __init__(self):
         Logger.debug("Horn created")

    def sound(self):
        Logger.debug("Horn sounded")
