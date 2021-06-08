import tkinter as tk
import random

width, height = 800, 800
arena_size_x = 12
arena_size_y = 12
margin = 30

ca = tk.Canvas(width=width, height=height)
ca.pack()


class Cell:
    def __init__(self, rect_id):
        self.rect_id = rect_id
        self.content = ''


class Game:
    def __init__(self):
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

        body_dir = random.choice(['L', 'R', 'U', 'D'])
        if body_dir in ('L', 'R'):
            sign = -1 if body_dir == 'L' else 1
            x = self.update_pos(self.head_x, sign, arena_size_x)
            self.set_state(x, self.head_y, 'B')
            x = self.update_pos(x, sign, arena_size_x)
            self.set_state(x, self.head_y, 'B')
        else:
            sign = -1 if body_dir == 'U' else 1
            y = self.update_pos(self.head_y, sign, arena_size_y)
            self.set_state(self.head_x, y, 'B')
            y = self.update_pos(y, sign, arena_size_y)
            self.set_state(self.head_x, y, 'B')

        self.add_apple()

    def set_state(self, x, y, part):
        color = None
        if part == 'H':  # head
            color = 'black'
        elif part == 'B':  # body
            color = 'gray'
        elif part == 'A':  # apple
            color = 'red'
        else:
            color = 'white'  # empty

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


game = Game()
ca.mainloop()
