import tkinter as tk
import random
import time
import numpy as np
from numpy import savetxt

from Controllers import BaseController, NaiveRandomController, RandomController, KeyboardController

EMPTY = '0'
APPLE = '1'
BODY = '2'
HEAD = '3'

width, height = 800, 800
arena_size = 5
margin = 30

ca = tk.Canvas(width=width, height=height, bg='whitesmoke')
ca.pack()


class Cell:
    def __init__(self, canvas, id, rect_id, text_id):
        self.canvas = canvas
        self.id = id
        self.rect_id = rect_id
        self.text_id = text_id
        self.content = EMPTY

    def set_title(self, msg):
        self.canvas.itemconfig(self.text_id, text=msg)


class Game:
    def __init__(self, canvas):
        self.game_state = 'P'
        self.bodies = []
        self.canvas = canvas
        self.csv_file_name = None
        dx = (width - 2 * margin) / arena_size
        dy = (height - 2 * margin) / arena_size
        dx = min(dx, dy)
        dy = min(dx, dy)
        self.arena = [[None for x in range(arena_size)]
                      for y in range(arena_size)]

        idx = 0
        for y in range(arena_size):
            for x in range(arena_size):
                x0 = x * dx + margin
                y0 = y * dy + margin
                r_id = ca.create_rectangle(x0, y0, x0 + dx, y0 + dy)
                t_id = ca.create_text(x0 + dx / 2, y0 + dy / 2, fill="dodgerblue")
                ca.create_text(x0 + 10, y0 + 10, text=str(idx), fill="black")
                cell = Cell(ca, idx, r_id, t_id)
                self.arena[y][x] = cell
                idx += 1

        self.head_x = random.randrange(arena_size)
        self.head_y = random.randrange(arena_size)
        self.set_state(self.head_x, self.head_y, HEAD)

        self.actual_heading = random.choice(['L', 'R', 'U', 'D'])
        if self.actual_heading in ('L', 'R'):
            sign = 1 if self.actual_heading == 'L' else -1
            x = self.add_position(self.head_x, sign, arena_size)
            self.bodies.append((x, self.head_y))
            self.set_state(x, self.head_y, BODY)

            x = self.add_position(x, sign, arena_size)
            self.bodies.append((x, self.head_y))
            self.set_state(x, self.head_y, BODY)
        else:
            sign = 1 if self.actual_heading == 'U' else -1
            y = self.add_position(self.head_y, sign, arena_size)
            self.bodies.append((self.head_x, y))
            self.set_state(self.head_x, y, BODY)

            y = self.add_position(y, sign, arena_size)
            self.bodies.append((self.head_x, y))
            self.set_state(self.head_x, y, BODY)

        self.add_apple()
        self.show_state()

    def set_state(self, x, y, part):
        color = None
        if part == HEAD:  # head
            color = 'gray'
        elif part == BODY:  # body
            color = 'silver'
        elif part == APPLE:  # apple
            color = 'red'
        elif part == EMPTY:  # empty
            color = 'whitesmoke'
        else:
            raise Exception('bad part')

        a = self.arena[y][x]
        a.content = part
        ca.itemconfig(a.rect_id, fill=color)

    def add_apple(self):
        while True:
            x = random.randrange(arena_size)
            y = random.randrange(arena_size)
            if self.arena[y][x].content == EMPTY:
                self.set_state(x, y, APPLE)
                break

    def add_position(self, val, add_val, limit):
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
            x = self.add_position(x, -1, arena_size)
        elif new_heading == 'R':
            x = self.add_position(x, 1, arena_size)
        elif new_heading == 'U':
            y = self.add_position(y, -1, arena_size)
        else:
            y = self.add_position(y, 1, arena_size)

        cell = self.arena[y][x]
        return x, y, new_heading, cell

    def execute(self, command):

        x, y, new_heading, cell = self.get_pos_info(command)
        cell_content = cell.content

        self.set_state(self.head_x, self.head_y, BODY)
        # hlava sa stava telom a ma sa dostat na prve miesto pola
        self.bodies.insert(0, (self.head_x, self.head_y))
        self.head_x, self.head_y = x, y
        self.set_state(self.head_x, self.head_y, HEAD)

        self.actual_heading = new_heading

        if cell_content != APPLE:
            x, y = self.bodies.pop()  # posledny kusok mizne, ale nie ak sa zedlo jabko
            self.set_state(x, y, EMPTY)
        else:
            self.add_apple()

        self.show_state()

    def show_state(self):
        pass
        #print(f"({self.head_x}, {self.head_y}), actual_heading: {self.actual_heading}")


    def clear_messages(self):
        for y in range(arena_size):
            for x in range(arena_size):
                self.arena[y][x].set_title(None)
        # -1: from left
        # 0: from ahead
        # 1: from right
    def show_input_data(self):
        self.clear_messages()
        count = arena_size * arena_size
        head = self.arena[self.head_y][self.head_x]
        head_idx = head.id
        start_y = head.id // arena_size
        start_x = head.id % arena_size
        node = None

        if self.actual_heading == 'L':
            mode = 'y'
            dif1 = 1
            dif2 = -1

        idx = 0
        x = start_x
        y = start_y
        while True:
            if mode == 'y':
                y += dif1
                if y >= arena_size:
                    y = 0
                    x += dif2
                    if x < 0:
                        x = arena_size - 1

            self.arena[y][x].set_title(str(idx))
            idx += 1
            if idx > count - 2:
                break;

    def get_content(self, command):
        x, y, new_heading, cell = self.get_pos_info(command)
        return cell.content

    def start_write_csv(self):
        self.csv_file_name = f"snake_rows({arena_size})_cols({arena_size})_{time.time()}.csv"

        print(self.csv_file_name)
        # print(strng)

    def write_row_to_csv(self):

        data = []
        for y in range(arena_size):
            for x in range(arena_size):
                data = self.arena[y][x].con
        np_arr = np.array(self.arena)
        np_flat = np.concatenate(np_arr)
        flat_str = np.char.mod('%d', np_flat).tolist()
        strng = ';'.join(flat_str)

        with open(self.csv_file_name, "a") as myfile:
            myfile.write("appended text")

#        savetxt('data.csv', anu, delimiter=',')
#        savetxt('data.csv', anu, delimiter=',')


game = Game(ca)
# ctl = RandomController(game, 100)
# ctl = NaiveRandomController(game, 100)
ctl = KeyboardController(game)
ca.mainloop()
