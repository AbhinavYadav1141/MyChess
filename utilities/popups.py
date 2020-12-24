from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder


Builder.load_file("utilities/popups.kv")


class PromotionPopupW(Popup):

    def __init__(self, command, move, i, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.command = command
        self.move = move
        self.i = i


class PromotionPopupB(Popup):

    def __init__(self, command, move, i, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.command = command
        self.move = move
        self.i = i
