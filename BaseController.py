import random


class BaseController:
    def __init__(self, _game):
        self.game = _game

    def next_move(self):
        pass


class RandomController(BaseController):

    def __init__(self, game, canvas, ticks):
        super().__init__(game)
        self.canvas = canvas
        self.ticks = ticks
        canvas.after(ticks, self.next_move)

    def next_move(self):
        cmd = random.randint(0, 2) - 1
        self.game.execute(cmd)
        self.canvas.after(self.ticks, self.next_move)
