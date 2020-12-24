from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.properties import ObjectProperty
import chess


Builder.load_file("main.kv")


class Manager(ScreenManager):
    mainscreen = ObjectProperty(None)
    gamescreen = ObjectProperty(None)


class ChessApp(App):
    manager = Manager()
    board = chess.Board()

    def build(self):
        return self.manager


if __name__ == "__main__":
    app = ChessApp()
    app.run()
