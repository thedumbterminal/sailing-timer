from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.clock import Clock, ClockEvent
from kivy.core.window import Window

from .temp_file import TempFile
from .log import Log
from .race import Race

Config.read("config.ini")

# Bluetooth "pointer" clickers are usually presentation remotes: they don't move a
# real cursor, they emit one of these keystrokes on each press.
POINTER_SPLIT_KEYS = {
    32,
    13,
    273,
    274,
    275,
    276,
    280,
    281,
}  # space, enter, arrows, page up/down


class SailingApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._race: Race
        self._start_button: Button
        self._stop_button: Button
        self._elapsed_time_label: Label
        self._elasped_interval: ClockEvent
        self._log: Log = Log(self)
        self._set_race()

    def _set_race(self):
        self._race = Race()
        self._race.get_events().bind(on_state_change=self._on_race_state_change)

    def _on_race_state_change(self, instance, old_state, new_state):
        self._log.debug("Race state changed")
        self.show_elapsed_time(0)  # Update immediately when state changes
        if self._race.is_running():
            self._start_button.disabled = False

        elif self._race.is_counting_down():
            self._start_button.disabled = True

    def show_elapsed_time(self, dt):
        self._log.debug("Updating elapsed time")
        elapsed_time = self._race.get_elapsed_time()
        num_splits = len(self._race.get_splits())
        num_countdowns = len(self._race.get_countdowns())
        self._elapsed_time_label.text = f"[{self._race.get_state()}] Elapsed: {str(elapsed_time).split('.')[0]} | Splits: {num_splits} | Countdowns: {num_countdowns}"

    def start_clicked(self, instance):
        self._log.debug("Start button clicked")
        instance.disabled = True

        self._race.countdown()
        self._stop_button.disabled = False
        self._elasped_interval = Clock.schedule_interval(
            self.show_elapsed_time, 5
        )  # Update elapsed time every second

    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        if key in POINTER_SPLIT_KEYS and not self._split_button.disabled:
            self._log.debug("Split triggered by pointer keypress")
            self._race.add_split()

    def _on_global_touch_down(self, window, touch):
        # Let the Start/Stop buttons handle their own clicks; anywhere else
        # counts as a split so you don't have to aim the pointer precisely.
        for widget in (self._start_button, self._stop_button):
            if widget.collide_point(*touch.pos):
                return
        if not self._split_button.disabled:
            self._log.debug("Split triggered by pointer click")
            self._race.add_split()

    def stop_clicked(self, instance):
        self._log.debug("Stop button clicked")
        instance.disabled = True
        Clock.unschedule(self._elasped_interval)
        self._race.stop()
        self._start_button.disabled = False
        temp_file = TempFile()
        self._race.export(temp_file.get_file())
        self._log.debug(f"Race results exported to {temp_file.get_file_name()}")
        # reset race for next run
        self._set_race()

    def build(self):
        layout = BoxLayout(padding=10, orientation="vertical")
        title = Label(text="Sailing Timer", font_size=36, size_hint=(1, 0.5))
        layout.add_widget(title)

        self._elapsed_time_label = Label(text="", font_size=16, size_hint=(1, 0.5))
        layout.add_widget(self._elapsed_time_label)

        self._start_button = Button(text="Start")
        self._start_button.bind(on_press=self.start_clicked)  # type: ignore[attr-defined]
        layout.add_widget(self._start_button)

        self._stop_button = Button(text="Stop", disabled=True)
        self._stop_button.bind(on_press=self.stop_clicked)  # type: ignore[attr-defined]
        layout.add_widget(self._stop_button)

        # Bluetooth pointer support: a click/keypress anywhere records a split.
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_touch_down=self._on_global_touch_down)

        return layout


if __name__ == "__main__":
    SailingApp().run()
