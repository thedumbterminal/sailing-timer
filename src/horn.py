from kivy.clock import Clock
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory
import platform

from .Log import Log

if platform.system() == "Darwin":
    from gpiozero.pins.mock import MockFactory

    Device.pin_factory = MockFactory()


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Horn:
    def __init__(self):
        self._pin = LED(20)
        self._log = Log(self)
        self._log.debug("Created")

    def sound(self):
        self._log.debug("Sounding")
        self._pin.on()
        Clock.schedule_once(self._stop, 5)

    def _stop(self, dt):
        self._pin.off()
        self._log.debug("Sounded")
