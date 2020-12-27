from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_file("utilities/pieces.kv")


class Piece(Widget):
    ptype = ""
    color = ""

    def __init__(self, color, position, ptype, variety: str = '1', **kwargs):
        super().__init__(**kwargs)

        self.ptype = ptype
        self.path = eval(open("data/piecespath.json").read())
        self.variety = variety
        self.color = color
        self._position = ""
        self.position = position
        self.active = False
        self.dots = []
        self.updater = Clock.schedule_interval(self.change, 3)
        # print("created")

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):

        self._position = position
        if self.parent is not None:
            self.change()

    '''
    def on_touch_down(self, touch):
        app = App.get_running_app()
        board = self.parent.board.board
        parent = self.parent
        if parent is not None:
            if (self.color == 'white' and board.turn is True) or (self.color == 'black' and board.turn is False):
                if eval(f"parent.board.{self.position}.collide_point(*touch.pos)"):
                    if not self.active:
                        self.active = True
                        self.add_dots()
                    else:
                        self.active = False
                        self.remove_dots()

                elif self.active:
                    blocks = parent.board.blocks
                    legal_moves = [str(i)[:4] for i in board.legal_moves]
                    for i in blocks.values():
                        move = self.position + i.name
                        if move in legal_moves:
                            if i.collide_point(*touch.pos):
                                if self.ptype == 'pawn' and (self.position[-1] == '7' and self.color == "white" or
                                                             self.position[-1] == '2' and self.color == "black"):
                                    PromotionPopupW(command=self.promote, move=move,
                                                    i=i).open() if self.color == "white" else PromotionPopupB().open()
                                else:
                                    board.push_san(move)
                                    piece = parent.board.piece_at(i.name)
                                    if piece is not None:
                                        parent.board.pieces.remove(piece)
                                        parent.remove_widget(piece)
                                    self.position = i.name
                                    # self.change()
                                break
                    self.active = False
                    self.remove_dots()
                    # print(self.pos)
            super().on_touch_down(touch)
'''

    def change(self, *args):
        if self.parent is not None:
            block = eval(f"self.parent.board.{self.position}")
            self.pos = block.pos
            self.size = block.size
            for i in self.dots:
                i.change()

    def move(self, mv):
        parent = self.parent
        board = self.parent.board.board
        legal = board.legal_moves
        move = None
        for i in legal:
            if str(i) == mv:
                move = i
                break
        if board.is_castling(move):
            if str(move)[-2] == 'c':
                self.parent.board.piece_at('a' + str(move)[-1]).position = 'd' + str(move)[-1]
            elif str(move)[-2] == 'g':
                self.parent.board.piece_at('h' + str(move)[-1]).position = 'f' + str(move)[-1]
        board.push_san(mv)
        piece = parent.board.piece_at(mv[2:4])
        if piece is not None:
            piece.destroy()
        self.position = mv[2:4]

    def add_dots(self):
        if self.parent is not None:
            board = self.parent.board.board
            legal_pos = [str(i)[2:] for i in board.legal_moves if str(i)[0:2] == self.position]

            for i in legal_pos:
                if len(i) == 3:
                    i = i[:2]
                block = self.parent.board.blocks[i]
                dot = Dot(position=i, block=block)
                self.parent.add_widget(dot)
                self.dots.append(dot)

    def remove_dots(self):
        for i in self.dots:
            self.parent.remove_widget(i)
        self.dots.clear()

    def promote(self, piece2, move):
        parent = self.parent
        move += "n" if piece2 == 'knight' else piece2[0]
        # self.ptype = piece

        self.move(move)

        parent.board.pieces.remove(self)
        parent.remove_widget(self)
        parent.board.add_piece(self.color, move[2:4], piece2, variety=self.variety)

    def destroy(self):
        self.updater.cancel()
        self.remove_dots()
        self.parent.board.pieces.remove(self)
        self.parent.remove_widget(self)


class Dot(Widget):

    def __init__(self, position, block, **kwargs):
        super().__init__(**kwargs)

        self.position = position
        self.block = block
        self.pos = (self.block.center_x - self.width / 2, self.block.center_y - self.height / 2)

    def change(self):
        if self.parent is not None:
            self.pos = (self.block.center_x - self.width / 2, self.block.center_y - self.height / 2)
