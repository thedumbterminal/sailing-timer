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
        self._stop_button = None
        self._elapsed_time_label = None
        self._elasped_interval = None

    def show_elapsed_time(self, dt):
        Logger.debug("UI: Updating elapsed time")
        if self._race and self._race.isRunning():
            elapsed_time = self._race.getElapsedTime()
            self._elapsed_time_label.text = f"[{self._race.getState()}] Elapsed Time: {str(elapsed_time).split('.')[0]}"  # Show HH:MM:SS

    def start_clicked(self, instance):
        Logger.debug("UI: Start button clicked")
        instance.disabled = True
        self._race = Race()
        self._race.countdown()
        self._stop_button.disabled = False  # Enable stop button
        self._elasped_interval = Clock.schedule_interval(
            self.show_elapsed_time, 5
        )  # Update elapsed time every second
        self.show_elapsed_time(0)  # Update immediately

    def stop_clicked(self, instance):
        Logger.debug("UI: Stop button clicked")
        instance.disabled = True
        Clock.unschedule(self._elasped_interval)
        self._race.stop()
        self.show_elapsed_time(0)  # Update immediately
        self._start_button.disabled = False  # Re-enable start button

    def build(self):
        layout = BoxLayout(padding=10, orientation="vertical")
        title = Label(text="Sailing Timer", font_size=40, size_hint=(1, 0.5))
        layout.add_widget(title)

        self._start_button = Button(text="Start")
        self._start_button.bind(on_press=self.start_clicked)
        layout.add_widget(self._start_button)

        self._elapsed_time_label = Label(text="", font_size=20, size_hint=(1, 0.5))
        layout.add_widget(self._elapsed_time_label)

        self._stop_button = Button(text="Stop", disabled=True)
        self._stop_button.bind(on_press=self.stop_clicked)
        layout.add_widget(self._stop_button)

        return layout


if __name__ == "__main__":
    SailingApp().run()
