from kivy.app import App
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
