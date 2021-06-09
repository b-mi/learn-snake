import random


class BaseController:
    def __init__(self, _game):
        self.game = _game

    def next_move(self):
        pass


class RandomController(BaseController):

    def __init__(self, game, ticks):
        super().__init__(game)
        self.ticks = ticks
        self.game.canvas.after(ticks, self.next_move)

    def next_move(self):
        cmd = random.randint(0, 2) - 1
        self.game.execute(cmd)
        self.game.canvas.after(self.ticks, self.next_move)


class NaiveRandomController(BaseController):

    def __init__(self, game, ticks):
        super().__init__(game)
        self.ticks = ticks
        self.game.canvas.after(ticks, self.next_move)

    def next_move(self):
        cmd = None
        left_content = self.game.get_content(-1)
        cmds = []
        if left_content == 'A':
            cmd = -1
        elif left_content != 'B':
            cmds.append(-1)
        
        forward_content = self.game.get_content(0)
        if cmd == None:
            if forward_content == 'A':
                cmd = 0
            elif forward_content != 'B':
                cmds.append(0)

        right_content = self.game.get_content(1)
        if cmd == None:
            if right_content == 'A':
                cmd = 1
            elif right_content != 'B':
                cmds.append(1)

        # print('choices', cmd, cmds)

        if cmd == None and len(cmds):
            cmd = random.choice(cmds)

        if cmd == None:
            self.game.game_state = 'L'
            pass  # end
        else:
            self.game.execute(cmd)
            self.game.canvas.after(self.ticks, self.next_move)
