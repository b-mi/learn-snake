import random
from Enums import Enums

class BaseController:
    def __init__(self, _game):
        self.game = _game

    def next_move(self):
        pass

class KeyboardController(BaseController):
    def __init__(self, _game):
        super().__init__(_game)
        self.game.canvas.focus_set()
        self.game.canvas.bind('<Left>', self.move)
        self.game.canvas.bind('<Right>', self.move)
        self.game.canvas.bind('<Up>', self.move)
        self.game.canvas.bind('<Down>', self.move)
        self.game.canvas.bind('<Return>', self.show_data)
        self.game.start_write_csv()

    def show_data(self, event):
        self.game.show_input_data()

    def move(self, event):
        cmd = None
        ask = event.keysym[0] # L, R, U, D
        act = self.game.actual_heading # L, R, U, D

        if ask == Enums.LEFT: # chce ist do lava
            if act ==  Enums.UP:
                cmd = -1
            elif act ==  Enums.DOWN:
                cmd = 1
            else:
                cmd = 0
        elif ask ==  Enums.RIGHT: # chce is doprava
            if act ==  Enums.UP:
                cmd = 1
            elif act ==  Enums.DOWN:
                cmd = -1
            else:
                cmd = 0
        elif ask ==  Enums.UP: # chce ist hore
            if act ==  Enums.LEFT:
                cmd = 1
            elif act ==  Enums.RIGHT:
                cmd = -1
            else:
                cmd = 0                
        elif ask == 'D': # chce ist dole
            if act ==  Enums.LEFT:
                cmd = -1
            elif act ==  Enums.RIGHT:
                cmd = 1
            else:
                cmd = 0                

        self.game.execute(cmd)




