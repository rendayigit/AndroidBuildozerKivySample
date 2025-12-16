from kivy.app import App
from kivy.uix.label import Label

class SimpleApp(App):
    def build(self):
        return Label(text="Hello from Python on Android!")

SimpleApp().run()   
