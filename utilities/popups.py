from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder


Builder.load_file("utilities/popups.kv")


class Data:
    def __init__(self, move, piece):
        self.auto_dismiss = False
        self.move = move
        self.piece = piece


class PromotionPopup(Popup, Data):
    pass
