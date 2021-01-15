from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from screens.gamescreen import GameScreen
from utilities.popups import ConfirmPopup

Builder.load_file("main.kv")


class TGLButton(ToggleButton):
    pass


class MainLayout(BoxLayout):
    btns = ObjectProperty(None)


class Manager(ScreenManager):
    mainscreen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.home_btn = None
        self.games = []
        self.l2 = None
        self.btn = None

    def new_game(self):
        if not self.games:
            self.home_btn = TGLButton(text=f"Home", on_press=lambda bt: self.change_scr(bt, "mainscreen"))
            self.home_btn.group = "screens"
            self.home_btn.allow_no_selection = False
            self.l2.add_widget(self.home_btn)
        name = f"gamescreen{len(self.games)+1}"
        self.games.append(GameScreen(name=name))
        self.add_widget(self.games[-1])

        self.btn = TGLButton(text=f"{len(self.games)}", on_release=lambda bt: self.change_scr(bt, name))
        self.btn.group = "screens"
        self.l2.add_widget(self.btn)
        self.games[-1].btn = self.btn
        self.btn.trigger_action(.01)
        self.btn.allow_no_selection = False
        # self.transition.direction = 'left'
        # self.current = name

    def change_scr(self, btn, scr):
        if scr == "mainscreen":
            self.transition.direction = "right"
        elif self.current == "mainscreen" or self.current[-1] < scr[-1]:
            self.transition.direction = "left"
        elif self.current[-1] > scr[-1]:
            self.transition.direction = "right"
        else:
            return

        self.current = scr


class ChessApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.manager = None
        self.layout = MainLayout(orientation="vertical")
        Clock.schedule_once(self.init)

    def init(self, dt):

        self.manager = Manager()
        self.manager.l2 = self.layout.btns
        self.layout.add_widget(self.manager)

    def build(self):
        Window.bind(on_keyboard=self._keyboard_down)
        return self.layout

    def _keyboard_down(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 == 27:
            if self.manager.current == 'mainscreen':
                ConfirmPopup(msg="Do you really want to quit?", yes_pressed=self.stop).open()
            else:
                self.manager.home_btn.trigger_action(.01)
            return True

        return False


if __name__ == "__main__":
    app = ChessApp()
    app.run()
