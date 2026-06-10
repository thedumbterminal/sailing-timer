from kivy.app import App
from kivy.uix.label import Label


class SailingApp(App):
    def build(self):
        return Label(text='Sailing app')

if __name__ == '__main__':
    SailingApp().run()
