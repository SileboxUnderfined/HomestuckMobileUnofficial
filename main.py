import kivy
kivy.require('2.0.0')

from kivymd.app import MDApp as App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager  import ScreenManager
from kivy.lang import Builder

from ui.mainMenu import MenuScreen
from ui.gameScreen import GameScreen

def builderLoader():
    Builder.load_file("ui/mainMenu.kv")
    Builder.load_file("ui/gameScreen.kv")

class MyApp(App):
    def screens(self):
        self.sm.add_widget(MenuScreen(name="menu"))
        self.sm.add_widget(GameScreen(name="game", page=1, autoSaveEnabled=False))

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.sm = ScreenManager()
        self.screens()
        return self.sm

def fontsInitializer():
    LabelBase.register(name="CubicPixel", fn_regular='ui/fonts/CubicPixel.otf')
    LabelBase.register(name="BreakPassword",fn_regular='ui/fonts/BreakPassword.otf')
    LabelBase.register(name="CourierNew",fn_regular='ui/fonts/CourierNew.ttf',fn_bold='ui/fonts/CourierNewBold.ttf')

if __name__ in "__main__":
    fontsInitializer()
    builderLoader()
    MyApp().run()