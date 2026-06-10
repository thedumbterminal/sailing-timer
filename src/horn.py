from kivy.logger import Logger


class Horn:
    def __init__(self):
        Logger.debug("Horn: Created")

    def sound(self):
        Logger.debug("Horn: Sounded")
