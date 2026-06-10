from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from .race import Race
from kivy.logger import Logger

class SailingApp(App):
    def start_clicked(self, instance):
        Logger.debug("Start button clicked")
        self._race = Race()
        self._race.start()

    def stop_clicked(self, instance):
        Logger.debug("Stop button clicked")
        self._race.stop()

    def build(self):
        layout = BoxLayout(padding=10, orientation="vertical")
        title = Label(text="Sailing app")
        startButton = Button(text="Start")
        stopButton = Button(text="Stop")

        startButton.bind(on_press=self.start_clicked)
        stopButton.bind(on_press=self.stop_clicked)

        layout.add_widget(title)
        layout.add_widget(startButton)
        layout.add_widget(stopButton)
        return layout


if __name__ == "__main__":
    SailingApp().run()
