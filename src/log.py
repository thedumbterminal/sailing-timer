import logging
from kivy.logger import KivyFormatter, Logger

for handler in logging.root.handlers:
    old_formatter = handler.formatter
    if isinstance(old_formatter, KivyFormatter):
        use_color = old_formatter._coloring_cls.__name__ == "ColoredLogRecord"
        new_fmt = "%(asctime)s " + old_formatter._fmt
        handler.setFormatter(KivyFormatter(new_fmt, use_color=use_color))

class Log:
    def __init__(self, instance):
        self._name = type(instance).__name__

    def debug(self, message):
        Logger.debug(self._name + ": " + message)   