from kivy.logger import Logger
from kivy.clock import Clock
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory
import platform

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
        Logger.debug("Horn: Created")

    def sound(self):
        Logger.debug("Horn: Sounding")
        self._pin.on()
        Clock.schedule_once(self._stop, 5)

    def _stop(self, dt):
        self._pin.off()
        Logger.debug("Horn: Sounded")
