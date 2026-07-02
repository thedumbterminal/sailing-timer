from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from .race import Race
from kivy.logger import Logger
from kivy.clock import Clock


class SailingApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._race = None
        self._start_button = None
        self._split_button = None
        self._stop_button = None
        self._elapsed_time_label = None
        self._elasped_interval = None

    def _on_race_state_change(self, instance, old_state, new_state):
        Logger.debug(f"UI: Race state changed")
        self.show_elapsed_time(0)  # Update immediately when state changes
        if self._race.is_running():
            self._split_button.disabled = False

    def show_elapsed_time(self, dt):
        Logger.debug("UI: Updating elapsed time")
        elapsed_time = self._race.get_elapsed_time()
        num_splits = len(self._race.get_splits())
        self._elapsed_time_label.text = f"[{self._race.get_state()}] Elapsed Time: {str(elapsed_time).split('.')[0]} | Splits: {num_splits}"

    def start_clicked(self, instance):
        Logger.debug("UI: Start button clicked")
        instance.disabled = True
        self._race = Race()
        self._race.get_events().bind(on_state_change=self._on_race_state_change)

        self._race.countdown()
        self._stop_button.disabled = False
        self._elasped_interval = Clock.schedule_interval(
            self.show_elapsed_time, 5
        )  # Update elapsed time every second

    def split_clicked(self, instance):
        Logger.debug("UI: Split button clicked")
        self._race.add_split()

    def stop_clicked(self, instance):
        Logger.debug("UI: Stop button clicked")
        instance.disabled = True
        Clock.unschedule(self._elasped_interval)
        self._race.stop()
        self._start_button.disabled = False
        self._split_button.disabled = True

    def build(self):
        layout = BoxLayout(padding=10, orientation="vertical")
        title = Label(text="Sailing Timer", font_size=40, size_hint=(1, 0.5))
        layout.add_widget(title)

        self._elapsed_time_label = Label(text="", font_size=20, size_hint=(1, 0.5))
        layout.add_widget(self._elapsed_time_label)

        self._start_button = Button(text="Start")
        self._start_button.bind(on_press=self.start_clicked)
        layout.add_widget(self._start_button)

        self._split_button = Button(text="Split", disabled=True)
        self._split_button.bind(on_press=self.split_clicked)
        layout.add_widget(self._split_button)

        self._stop_button = Button(text="Stop", disabled=True)
        self._stop_button.bind(on_press=self.stop_clicked)
        layout.add_widget(self._stop_button)

        return layout


if __name__ == "__main__":
    SailingApp().run()
