import kivy
kivy.require('2.0.0')

from kivy.app import App
from ui.mainMenu import MainMenu


class MyApp(App):
    def build(self):
        return MainMenu()

if __name__ in "__main__":
    MyApp().run()