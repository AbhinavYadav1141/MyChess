import chess
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from utilities.pieces import Piece
from utilities.popups import PromotionPopup


class Data:
    def __init__(self, source, name):
        self.source = source
        self.name = name


class Block(Widget, Data):
    pass


class ChessLayout(GridLayout):
    mainlayout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 8
        self.blocks = {}
        self.pieces = []
        self.active = False
        self.active_piece = None

        for i in range(7, -1, -1):
            for j in range(8):
                source = "assets/images/white.png" if (i + j) % 2 == 1 else "assets/images/black.png"
                name = f"{chr(97 + j)}{i + 1}"
                exec(f"self.{name}=Block(source=source, name=name)")
                self.add_widget(eval(f"self.{name}"))
                self.blocks[name] = eval(f"self.{name}")

    def add_piece(self, color, position, ptype, variety='1'):
        pc = Piece(color=color, position=position, ptype=ptype, variety=variety)
        self.mainlayout.add_widget(pc)
        self.pieces.append(pc)
        block = eval(f"self.{position}")
        pc.pos = block.pos
        pc.size = block.size
        self.mainlayout.bind(pos=pc.change)
        self.mainlayout.bind(size=pc.change)
        # print("added")

    def start(self, btn):
        variety = '2'
        for i in range(8):
            self.add_piece("white", chr(97 + i) + '2', "pawn", variety)
        for i in range(8):
            self.add_piece("black", chr(97 + i) + '7', "pawn", variety)
        self.add_piece("white", 'a1', "rook", variety)
        self.add_piece("white", 'b1', "knight", variety)
        self.add_piece("white", 'c1', "bishop", variety)
        self.add_piece("white", 'd1', "queen", variety)
        self.add_piece("white", 'e1', "king", variety)
        self.add_piece("white", 'f1', "bishop", variety)
        self.add_piece("white", 'g1', "knight", variety)
        self.add_piece("white", 'h1', "rook", variety)
        self.add_piece("black", 'a8', "rook", variety)
        self.add_piece("black", 'b8', "knight", variety)
        self.add_piece("black", 'c8', "bishop", variety)
        self.add_piece("black", 'd8', "queen", variety)
        self.add_piece("black", 'e8', "king", variety)
        self.add_piece("black", 'f8', "bishop", variety)
        self.add_piece("black", 'g8', "knight", variety)
        self.add_piece("black", 'h8', "rook", variety)

        btn.disabled = True

    def piece_at(self, square):
        for i in self.pieces:
            if i.position == square:
                return i

    def on_touch_down(self, touch):
        app = App.get_running_app()
        board: chess.Board = app.board

        block = None
        piece = None
        active_piece = self.active_piece

        for i in self.blocks:
            if self.blocks[i].collide_point(*touch.pos):
                block = self.blocks[i]
                break

        if not self.active:
            if block is not None:
                for i in self.pieces:
                    if i.position == block.name:
                        piece = i
                        break
                if piece is not None:
                    self.active = True
                    self.active_piece = piece
                    self.active_piece.add_dots()
        else:
            if block is not None:
                legal_moves = [str(i) for i in board.legal_moves]
                move = active_piece.position + block.name
                if move in legal_moves:
                    active_piece.move(move)
                elif active_piece.ptype == "pawn":

                    if active_piece.position[1] == '7' and active_piece.color == "white" \
                            or active_piece.position[1] == '2' and active_piece.color == "black":
                        PromotionPopup(move=move, piece=active_piece).open()

            active_piece.remove_dots()
            self.active = False
            self.active_piece = None
        super().on_touch_down(touch)


class GameScreen(Screen):
    board = ObjectProperty(None)


class GameScreenApp(App):

    def build(self):
        return GameScreen()


if __name__ == '__main__':
    Builder.load_file('gamescreen.kv')
    GameScreenApp().run()
else:
    Builder.load_file("screens/gamescreen.kv")
