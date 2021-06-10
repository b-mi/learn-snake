import tkinter as tk
import random

from Controllers import BaseController, NaiveRandomController, RandomController, KeyboardController

width, height = 800, 800
arena_size_x = 12
arena_size_y = 12
margin = 30

ca = tk.Canvas(width=width, height=height, bg='whitesmoke')
ca.pack()


class Cell:
    def __init__(self, rect_id):
        self.rect_id = rect_id
        self.content = ''


class Game:
    def __init__(self, canvas):
        self.game_state = 'P'
        self.bodies = []
        self.canvas = canvas
        dx = (width - 2 * margin) / arena_size_x
        dy = (height - 2 * margin) / arena_size_y
        dx = min(dx, dy)
        dy = min(dx, dy)
        self.arena = [[None for x in range(arena_size_x)] for y in range(arena_size_y)]

        for y in range(arena_size_y):
            for x in range(arena_size_x):
                x0 = x * dx + margin
                y0 = y * dy + margin
                r_id = ca.create_rectangle(x0, y0, x0 + dx, y0 + dy)
                cell = Cell(r_id)
                self.arena[y][x] = cell

        self.head_x = random.randrange(arena_size_x)
        self.head_y = random.randrange(arena_size_y)
        self.set_state(self.head_x, self.head_y, 'H')

        self.actual_heading = random.choice(['L', 'R', 'U', 'D'])
        if self.actual_heading in ('L', 'R'):
            sign = 1 if self.actual_heading == 'L' else -1
            x = self.update_pos(self.head_x, sign, arena_size_x)
            self.bodies.append((x, self.head_y))
            self.set_state(x, self.head_y, 'B')

            x = self.update_pos(x, sign, arena_size_x)
            self.bodies.append((x, self.head_y))
            self.set_state(x, self.head_y, 'B')
        else:
            sign = 1 if self.actual_heading == 'U' else -1
            y = self.update_pos(self.head_y, sign, arena_size_y)
            self.bodies.append((self.head_x, y))
            self.set_state(self.head_x, y, 'B')

            y = self.update_pos(y, sign, arena_size_y)
            self.bodies.append((self.head_x, y))
            self.set_state(self.head_x, y, 'B')

        self.add_apple()
        self.show_state()

    def set_state(self, x, y, part):
        color = None
        if part == 'H':  # head
            color = 'gray'
        elif part == 'B':  # body
            color = 'silver'
        elif part == 'A':  # apple
            color = 'red'
        else:
            color = 'whitesmoke'  # empty

        a = self.arena[y][x]
        a.content = part
        ca.itemconfig(a.rect_id, fill=color)

    def add_apple(self):
        while True:
            x = random.randrange(arena_size_x)
            y = random.randrange(arena_size_y)
            if not self.arena[y][x].content:
                self.set_state(x, y, 'A')
                break

    def update_pos(self, val, add_val, limit):
        return (val + add_val) % limit

    def get_pos_info(self, command):
        x = self.head_x
        y = self.head_y
        new_heading = ''
        if command == -1:  # left
            if self.actual_heading == 'L':
                new_heading = 'D'
            elif self.actual_heading == 'R':
                new_heading = 'U'
            elif self.actual_heading == 'U':
                new_heading = 'L'
            else:  # D
                new_heading = 'R'
        elif command == 1:  # right
            if self.actual_heading == 'L':
                new_heading = 'U'
            elif self.actual_heading == 'R':
                new_heading = 'D'
            elif self.actual_heading == 'U':
                new_heading = 'R'
            else:  # D
                new_heading = 'L'
        else:  # rovno
            new_heading = self.actual_heading

        if new_heading == 'L':
            x = self.update_pos(x, -1, arena_size_x)
        elif new_heading == 'R':
            x = self.update_pos(x, 1, arena_size_x)
        elif new_heading == 'U':
            y = self.update_pos(y, -1, arena_size_y)
        else:
            y = self.update_pos(y, 1, arena_size_y)

        cell = self.arena[y][x]
        return x, y, new_heading, cell

    def execute(self, command):

        x, y, new_heading, cell = self.get_pos_info(command)
        cell_content = cell.content

        self.set_state(self.head_x, self.head_y, 'B')
        self.bodies.insert(0, (self.head_x, self.head_y))  # hlava sa stava telom a ma sa dostat na prve miesto pola
        self.head_x, self.head_y = x, y
        self.set_state(self.head_x, self.head_y, 'H')

        self.actual_heading = new_heading

        if cell_content != 'A':
            x, y = self.bodies.pop()  # posledny kusok mizne, ale nie ak sa zedlo jabko
            self.set_state(x, y, None)
        else:
            self.add_apple()

        self.show_state()

    def show_state(self):
        pass
        #print(f"({self.head_x}, {self.head_y}), actual_heading: {self.actual_heading}")

        #-1: from left
        #0: from ahead
        #1: from right

    def get_content(self, command):
        x, y, new_heading, cell = self.get_pos_info(command)
        return cell.content


    def next(self):
        cmd = self.controller.get_direction()
        self.execute(cmd)


game = Game(ca)
# ctl = RandomController(game, 100)
# ctl = NaiveRandomController(game, 100)
ctl = KeyboardController(game)
ca.mainloop()
