from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from utilities.pieces import Piece


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

        for i in range(7, -1, -1):
            for j in range(8):
                source = "assets/images/white.png" if (i+j) % 2 == 1 else "assets/images/black.png"
                name = f"{chr(97+j)}{i+1}"
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


class GameScreen(Screen):
    board = ObjectProperty(None)


class GameScreenApp(App):

    def build(self):
        return GameScreen()


if __name__ == '__main__':
    Builder.load_file('gamescreen.kv')
    app = GameScreenApp()
    app.run()
else:
    Builder.load_file("screens/gamescreen.kv")
