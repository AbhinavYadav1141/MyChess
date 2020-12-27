import chess
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from utilities.pieces import Piece
from utilities.popups import PromotionPopup, ResultPopup


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
        self.board = chess.Board()

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
        # self.mainlayout.bind(pos=pc.change)
        # self.mainlayout.bind(size=pc.change)
        # print("added")

    def start(self, btn):
        btn.disabled = True
        ptype = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        variety = '2'
        for i in range(8):
            for j in (("white", '21'), ("black", '78')):
                self.add_piece(j[0], chr(97 + i) + j[1][0], "pawn", variety)
                self.add_piece(j[0], chr(97 + i) + j[1][1], ptype[i], variety)

    def restart(self, btn):
        btn.disabled = True
        self.board = chess.Board()
        for i in self.pieces:
            i.destroy()

        ch = list(self.children)
        for i in ch:
            self.remove_widget(i)

        for i in range(7, -1, -1):
            for j in range(8):
                name = f"{chr(97 + j)}{i + 1}"
                exec(f"del self.{name}")

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

        self.start(btn)

    def piece_at(self, square):
        for i in self.pieces:
            if i.position == square:
                return i

    def on_touch_down(self, touch):
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
                legal_moves = [str(i) for i in self.board.legal_moves]
                move = active_piece.position + block.name
                if move in legal_moves:
                    active_piece.move(move)
                elif active_piece.ptype == "pawn" and move in [i[:4] for i in legal_moves]:

                    if active_piece.position[1] == '7' and active_piece.color == "white" \
                            or active_piece.position[1] == '2' and active_piece.color == "black":
                        PromotionPopup(move=move, piece=active_piece).open()

            active_piece.remove_dots()

            gameover = self.gameover(self.board)
            if gameover[0]:
                ResultPopup(result=gameover[1], reason=gameover[2], restart=self.restart).open()

            self.active = False
            self.active_piece = None
        super().on_touch_down(touch)

    def gameover(self, board):
        reason = ""
        result = ""
        check = False
        if board.is_game_over():
            check = True
            result = "0.5 - 0.5"
            reason = "Unknown Reason"

        if board.is_checkmate():
            reason = "Checkmate"
            result = "0-1" if board.turn else "1-0"
        elif board.is_fivefold_repetition():
            reason = "five fold repetition"
        elif board.is_insufficient_material():
            reason = "Insufficient material"
        elif board.is_stalemate():
            reason = "Stalemate"
        elif board.is_seventyfive_moves():
            reason = "Seventy Five Moves"
        elif board.is_variant_draw():
            reason = "Variant draw"

        return check, result, reason


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
