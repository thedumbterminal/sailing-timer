from kivy.logger import Logger
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory
from time import sleep
import platform

if platform.system() == "Darwin":
    from gpiozero.pins.mock import MockFactory

    Device.pin_factory = MockFactory()


class Horn:
    def __init__(self):
        self._pin = LED(20)
        Logger.debug("Horn: Created")

    def sound(self):
        Logger.debug("Horn: Sounding")
        self._pin.on()
        sleep(5)
        self._pin.off()
        Logger.debug("Horn: Sounded")
