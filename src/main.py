from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class SailingApp(App):
    def build(self):    
        layout = BoxLayout(padding=10, orientation='vertical')
        title = Label(text='Sailing app')
        startButton = Button(text='Start')
        layout.add_widget(title)
        layout.add_widget(startButton)
        return layout

if __name__ == '__main__':
    SailingApp().run()
