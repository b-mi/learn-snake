import tkinter as tk
import random
import time
import numpy as np
from numpy import savetxt
from Enums import Enums

from Controllers import BaseController, KeyboardController

width, height = 800, 800
arena_size = 9
margin = 30
refl_depth = (arena_size-1) // 2

ca = tk.Canvas(width=width, height=height, bg='whitesmoke')
ca.pack()


class Cell:
    def __init__(self, canvas, id, rect_id, text_id, text2_id):
        self.canvas = canvas
        self.id = id
        self.rect_id = rect_id
        self.text_id = text_id
        self.text2_id = text2_id
        self.content = Enums.EMPTY

    def set_title(self, msg):
        self.canvas.itemconfig(self.text_id, text=msg)

    def set_title2(self, msg):
        self.canvas.itemconfig(self.text2_id, text=msg)


class Game:
    def __init__(self, canvas):
        self.game_state = Enums.PLAY
        self.bodies = []
        self.canvas = canvas
        self.csv_file_name = None
        self.apples_eaten = 0
        self.cells_count = arena_size * arena_size
        dx = (width - 2 * margin) / arena_size
        dy = (height - 2 * margin) / arena_size
        dx = min(dx, dy)
        dy = min(dx, dy)
        self.arena = [[None for x in range(arena_size)]
                      for y in range(arena_size)]

        self.inp_inst = {}
        # diff1, diff2, diff3  posun jednej suradnice, druhej suradnice, pri iteracii
        self.inp_inst[Enums.LEFT] = ('x', -1, 1, -1)
        self.inp_inst[Enums.RIGHT] = ('x', 1, -1, 1)
        self.inp_inst[Enums.UP] = ('y', -1, -1, 1)
        self.inp_inst[Enums.DOWN] = ('y', 1, 1, -1)

        self.rot_left = {}
        self.rot_left[Enums.LEFT] = Enums.DOWN
        self.rot_left[Enums.RIGHT] = Enums.UP
        self.rot_left[Enums.UP] = Enums.LEFT
        self.rot_left[Enums.DOWN] = Enums.RIGHT

        self.rot_right = {}
        self.rot_right[Enums.LEFT] = Enums.UP
        self.rot_right[Enums.RIGHT] = Enums.DOWN
        self.rot_right[Enums.UP] = Enums.RIGHT
        self.rot_right[Enums.DOWN] = Enums.LEFT

        idx = 0
        for y in range(arena_size):
            for x in range(arena_size):
                x0 = x * dx + margin
                y0 = y * dy + margin
                r_id = ca.create_rectangle(x0, y0, x0 + dx, y0 + dy)
                t_id = ca.create_text(
                    x0 + dx / 2, y0 + dy / 2, fill="dodgerblue")
                ca.create_text(x0 + 30, y0 + 10,
                               text=f"{str(idx)}, ({x}, {y})", fill="black")
                t2_id = ca.create_text(
                    x0 + 10, y0 + dy - 10, fill="green", text='0')
                cell = Cell(ca, idx, r_id, t_id, t2_id)
                self.arena[y][x] = cell
                idx += 1

        self.head_x = random.randrange(arena_size)
        self.head_y = random.randrange(arena_size)
        self.set_cell_state(self.head_x, self.head_y, Enums.HEAD)

        self.actual_heading = random.choice(
            [Enums.LEFT, Enums.RIGHT, Enums.UP, Enums.DOWN])
        if self.actual_heading in (Enums.LEFT, Enums.RIGHT):
            sign = 1 if self.actual_heading == Enums.LEFT else -1
            x = self.add_position(self.head_x, sign, arena_size)
            self.bodies.append((x, self.head_y))
            self.set_cell_state(x, self.head_y, Enums.BODY)

            x = self.add_position(x, sign, arena_size)
            self.bodies.append((x, self.head_y))
            self.set_cell_state(x, self.head_y, Enums.BODY)
        else:
            sign = 1 if self.actual_heading == Enums.UP else -1
            y = self.add_position(self.head_y, sign, arena_size)
            self.bodies.append((self.head_x, y))
            self.set_cell_state(self.head_x, y, Enums.BODY)

            y = self.add_position(y, sign, arena_size)
            self.bodies.append((self.head_x, y))
            self.set_cell_state(self.head_x, y, Enums.BODY)

        self.add_apple()

    def set_cell_state(self, x, y, part):
        color = None
        if part == Enums.HEAD:  # head
            color = 'gray'
        elif part == Enums.BODY:  # body
            color = 'silver'
        elif part == Enums.APPLE:  # apple
            color = 'red'
        elif part == Enums.EMPTY:  # empty
            color = 'whitesmoke'
        else:
            raise Exception('bad part')

        cell = self.arena[y][x]
        cell.content = part
        ca.itemconfig(cell.rect_id, fill=color)
        cell.set_title2(part)

    def add_apple(self):
        while True:
            x = random.randrange(arena_size)
            y = random.randrange(arena_size)
            if self.arena[y][x].content == Enums.EMPTY:
                self.set_cell_state(x, y, Enums.APPLE)
                break

    def add_position(self, val, add_val, limit):
        return (val + add_val) % limit

    def get_pos_info(self, command):
        x = self.head_x
        y = self.head_y
        new_heading = ''
        if command == -1:  # left
            if self.actual_heading == Enums.LEFT:
                new_heading = Enums.DOWN
            elif self.actual_heading == Enums.RIGHT:
                new_heading = Enums.UP
            elif self.actual_heading == Enums.UP:
                new_heading = Enums.LEFT
            else:  # D
                new_heading = Enums.RIGHT
        elif command == 1:  # right
            if self.actual_heading == Enums.LEFT:
                new_heading = Enums.UP
            elif self.actual_heading == Enums.RIGHT:
                new_heading = Enums.DOWN
            elif self.actual_heading == Enums.UP:
                new_heading = Enums.RIGHT
            else:  # D
                new_heading = Enums.LEFT
        else:  # rovno
            new_heading = self.actual_heading

        if new_heading == Enums.LEFT:
            x = self.add_position(x, -1, arena_size)
        elif new_heading == Enums.RIGHT:
            x = self.add_position(x, 1, arena_size)
        elif new_heading == Enums.UP:
            y = self.add_position(y, -1, arena_size)
        else:
            y = self.add_position(y, 1, arena_size)

        cell = self.arena[y][x]
        return x, y, new_heading, cell

    def execute(self, command):

        if self.game_state == Enums.LOSS:
            print('LOSS')
            return
        elif self.game_state == Enums.WIN:
            print('WIN')
            return

        data_to_csv = self.get_csv_row(command)

        x, y, new_heading, cell = self.get_pos_info(command)
        cell_content = cell.content

        self.set_cell_state(self.head_x, self.head_y, Enums.BODY)
        # hlava sa stava telom a ma sa dostat na prve miesto pola
        self.bodies.insert(0, (self.head_x, self.head_y))
        self.head_x, self.head_y = x, y
        self.set_cell_state(self.head_x, self.head_y, Enums.HEAD)

        self.actual_heading = new_heading

        if cell_content == Enums.BODY:
            self.game_state = Enums.LOSS
        if cell_content != Enums.APPLE:
            x, y = self.bodies.pop()  # posledny kusok mizne, ale nie ak sa zedlo jabko
            self.set_cell_state(x, y,  Enums.EMPTY)
        else:
            self.apples_eaten += 1
            if self.apples_eaten == self.cells_count - 3:
                self.game_state = Enums.WIN
                print('WIN')
            else:
                self.add_apple()
        if self.game_state == Enums.PLAY:
            self.append_row_to_csv(data_to_csv)


    def append_row_to_csv(self, csv_array):
        sout = ','.join(csv_array) + '\n'
        with open(self.csv_file_name, "a") as myfile:
            myfile.write(sout)

    def get_csv_row(self, command):
        out_arr = []
        from_front = self.get_input_data(Enums.FROM_FRONT)
        from_left = self.get_input_data(Enums.FROM_LEFT)
        from_right = self.get_input_data(Enums.FROM_RIGHT)
        for part in (from_left, from_front, from_right):
            for cell in part:
                out_arr.append(cell.content)
        out_arr.append(str(command))
        return out_arr


    def clear_messages(self):
        for y in range(arena_size):
            for x in range(arena_size):
                self.arena[y][x].set_title('')
        # -1: from left
        # 0: from ahead
        # 1: from right

    def get_input_data(self, xfrom):

        hdg = None
        if xfrom == Enums.FROM_FRONT:
            hdg = self.actual_heading
        elif xfrom == Enums.FROM_LEFT:
            hdg = self.rot_left[self.actual_heading]
        elif xfrom == Enums.FROM_RIGHT:
            hdg = self.rot_right[self.actual_heading]
        else:
            raise Exception()

        instr = self.inp_inst[hdg]

        cells = []
        cell_cnt = 3
        x, y = self.head_x, self.head_y
        mode, diff1, diff2, diff3 = instr
        for i in range(refl_depth):
            x = self.add_position(x, diff1, arena_size)
            y = self.add_position(y, diff2, arena_size)
            _x, _y = x, y
            for j in range(cell_cnt):
                cells.append(self.arena[_y][_x])
                if mode == 'y':
                    _x = self.add_position(_x, diff3, arena_size)
                else:
                    _y = self.add_position(_y, diff3, arena_size)

            cell_cnt += 2

        idx = 0
        # self.clear_messages()
        # for c in cells:
        #     c.set_title(str(idx))
        #     idx += 1
        return cells

    def get_content(self, command):
        x, y, new_heading, cell = self.get_pos_info(command)
        return cell.content

    def start_write_csv(self):
        self.csv_file_name = f"snake_rows({arena_size})_cols({arena_size})_{time.time()}.csv"
        print(self.csv_file_name)
        # print(strng)

 
game = Game(ca)
# ctl = RandomController(game, 100)
# ctl = NaiveRandomController(game, 100)
ctl = KeyboardController(game)
ca.mainloop()
