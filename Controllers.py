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


class KeyboardController(BaseController):
    def __init__(self, _game):
        super().__init__(_game)
        self.game.canvas.focus_set()
        self.game.canvas.bind('<Left>', self.move)
        self.game.canvas.bind('<Right>', self.move)
        self.game.canvas.bind('<Up>', self.move)
        self.game.canvas.bind('<Down>', self.move)
        self.game.start_write_csv()

    def move(self, event):
        cmd = None
        ask = event.keysym[0] # L, R, U, D
        act = self.game.actual_heading # L, R, U, D

        if ask == 'L': # chce ist do lava
            if act == 'U':
                cmd = -1
            elif act == 'D':
                cmd = 1
            else:
                cmd = 0
        elif ask == 'R': # chce is doprava
            if act == 'U':
                cmd = 1
            elif act == 'D':
                cmd = -1
            else:
                cmd = 0
        elif ask == 'U': # chce ist hore
            if act == 'L':
                cmd = 1
            elif act == 'R':
                cmd = -1
            else:
                cmd = 0                
        elif ask == 'D': # chce ist dole
            if act == 'L':
                cmd = -1
            elif act == 'R':
                cmd = 1
            else:
                cmd = 0                

        self.game.execute(cmd)




