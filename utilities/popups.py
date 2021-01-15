from kivy.uix.popup import Popup
from kivy.lang import Builder

Builder.load_file("utilities/popups.kv")


class ProData:
    def __init__(self, move, piece):
        self.auto_dismiss = False
        self.move = move
        self.piece = piece


class PromotionPopup(Popup, ProData):
    pass


class ResData:
    def __init__(self, result, reason, restart):
        self.result = result
        self.reason = reason
        self.restart = restart


class ResultPopup(Popup, ResData):
    pass


class ConData:
    def __init__(self, msg='', yes_pressed=print, no_pressed=print, dismiss_on_press=True):
        self.msg = msg
        self.yes_pressed = yes_pressed
        self.no_pressed = no_pressed
        self.dismiss_on_press = dismiss_on_press


class ConfirmPopup(Popup, ConData):
    pass
