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
        self.mode = "Offline"  # Offline or Online
        self.color = None  # For online mode

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
        pieces = list(self.pieces)
        for i in pieces:
            i.destroy()

        ch = list(self.children)
        for i in ch:
            self.remove_widget(i)

        for i in range(7, -1, -1):
            for j in range(8):
                name = f"{chr(97 + j)}{i + 1}"
                exec(f"del self.{name}")

        self.blocks = {}
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

    def piece_at(self, square: str):
        for i in self.pieces:
            if i.position == square:
                return i

    def on_touch_down(self, touch):
        if self.mode == "Offline" or (
                                      self.mode == "Online" and
                                      ((self.board.turn and self.color == 'white') or
                                       not self.board.turn and self.color == 'black')
                                      ):
            self.move_self(touch.pos)
        super().on_touch_down(touch)

    def move_self(self, pos):
        block = None
        piece = None
        active_piece = self.active_piece

        for i in self.blocks:
            if self.blocks[i].collide_point(*pos):
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
                else:
                    piece = self.piece_at(block.name)
                    if piece is not None:
                        active_piece.remove_dots()
                        self.active_piece = piece
                        self.active_piece.add_dots()
                        return

            active_piece.remove_dots()

            self.active = False
            self.active_piece = None

            gameover = self.gameover(self.board)
            if gameover[0]:
                ResultPopup(result=gameover[1], reason=gameover[2], restart=self.restart).open()

    def move_other(self, move):   # for online mode only
        position = move[0:2]
        piece = self.piece_at(position)
        piece.move(move) if len(move) == 4 else piece.promote(move)

        gameover = self.gameover(self.board)
        if gameover[0]:
            ResultPopup(result=gameover[1], reason=gameover[2], restart=self.restart).open()

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

    def close(self, btn):
        btn.disabled = True
        gm = self.gamescreen
        gm.manager.l2.remove_widget(gm.btn)
        gm.manager.games.remove(gm)
        if len(gm.manager.games) == 0:
            gm.manager.l2.remove_widget(gm.manager.home_btn)
        else:
            gm.manager.current = f"gamescreen{int(gm.name[-1]) + 1}" \
                if gm.name[-1] == '1' else f"gamescreen{int(gm.name[-1]) - 1}"
        gm.manager.remove_widget(gm)


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
