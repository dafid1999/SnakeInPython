# Author: aqeelanwar
# Created: 12 June,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

# Icons: https://www.flaticon.com/authors/freepik
from tkinter import *
import random
import time
import numpy as np
from PIL import ImageTk, Image

# Define useful parameters
size_of_board = 1000
rows = 20
cols = 20
DELAY = 100
snake_initial_length = 3
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 2
RED_COLOR = "#EE4035"
BLUE_COLOR = "#0492CF"
Green_color = "#7BC043"

BLUE_COLOR_LIGHT = '#67B0CF'
RED_COLOR_LIGHT = '#EE7E77'


class SnakeAndApple:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title("Snake-and-Apple")
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks and keyboard
        self.window.bind("<Key>", self.key_input)
        self.window.bind("<Button-1>", self.mouse_input)
        self.play_again()
        self.begin = False

    def initialize_board(self):
        self.board = []
        self.apple_obj = []
        self.old_apple_cell = []

        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))

        for i in range(rows):
            self.canvas.create_line(
                i * size_of_board / rows, 0, i * size_of_board / rows, size_of_board,
            )

        for i in range(cols):
            self.canvas.create_line(
                0, i * size_of_board / cols, size_of_board, i * size_of_board / cols,
            )

    def initialize_snake(self):
        self.snake = []
        self.crashed = False
        self.snake_heading = "Right"
        self.last_key = self.snake_heading
        self.forbidden_actions = {}
        self.forbidden_actions["Right"] = "Left"
        self.forbidden_actions["Left"] = "Right"
        self.forbidden_actions["Up"] = "Down"
        self.forbidden_actions["Down"] = "Up"
        self.snake_objects = []
        for i in range(snake_initial_length):
            self.snake.append((i, 0))

    def initialize_enemy(self):
        self.enemy = []
        self.enemy_objects = []
        self.enemy_size = [(0, 0), (1, 1)]
        self.enemy_cell = []
        self.enemy_speed = 0
        self.enemy_level = 0

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.initialize_snake()
        self.place_apple()
        self.initialize_enemy()
        self.display_snake(mode="complete")
        self.display_enemy(mode="start")
        self.begin_time = time.time()

    def update(self):
        self.update_snake(self.last_key)
        self.update_enemy()

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                if not self.crashed:
                    self.window.after(DELAY, self.update())
                else:
                    self.begin = False
                    self.display_gameover()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------
    def display_gameover(self):
        score = len(self.snake)
        self.canvas.delete("all")
        score_text = "Scores \n"

        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10

        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 8,
            font="cmr 40 bold",
            fill=Green_color,
            text=score_text,
        )
        score_text = str(score)
        self.canvas.create_text(
            size_of_board / 2,
            1 * size_of_board / 2,
            font="cmr 50 bold",
            fill=BLUE_COLOR,
            text=score_text,
        )
        time_spent = str(np.round(time.time() - self.begin_time, 1)) + 'sec'
        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 4,
            font="cmr 20 bold",
            fill=BLUE_COLOR,
            text=time_spent,
        )
        score_text = "Click to play again \n"
        self.canvas.create_text(
            size_of_board / 2,
            15 * size_of_board / 16,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )

    def place_apple(self):
        # Place apple randomly anywhere except at the cells occupied by snake
        unoccupied_cels = set(self.board) - set(self.snake)
        self.apple_cell = random.choice(list(unoccupied_cels))
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=RED_COLOR_LIGHT, outline=BLUE_COLOR,
        )

    def display_snake(self, mode=""):
        # Remove tail from display if it exists
        if self.snake_objects != []:
            self.canvas.delete(self.snake_objects.pop(0))
        if mode == "complete":
            for i, cell in enumerate(self.snake):
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = cell[0] * row_h
                y1 = cell[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.append(
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=BLUE_COLOR, outline=BLUE_COLOR,
                    )
                )
        else:
            # only update head
            cell = self.snake[-1]
            row_h = int(size_of_board / rows)
            col_w = int(size_of_board / cols)
            x1 = cell[0] * row_h
            y1 = cell[1] * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            self.snake_objects.append(
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=BLUE_COLOR, outline=RED_COLOR,
                )
            )
            if self.snake[0] == self.old_apple_cell:
                self.snake.insert(0, self.old_apple_cell)
                self.old_apple_cell = []
                tail = self.snake[0]
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = tail[0] * row_h
                y1 = tail[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.insert(
                    0,
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=BLUE_COLOR, outline=RED_COLOR
                    ),
                )
            if self.check_collision(self.snake[-1], self.enemy_size[0], self.enemy_size[1]):
                self.crashed = TRUE
            self.window.update()

    def display_enemy(self, mode=""):
        if mode == "start":
            unoccupied_cells = set(self.board) - set(self.snake) - set(self.apple_cell)
            self.enemy_cell = random.choice(list(unoccupied_cells))
            self.enemy.insert(0, self.enemy_cell)
            self.enemy.insert(1, self.enemy_cell)
        else:
            self.canvas.delete(self.enemy_objects[-1])
            self.enemy_objects.pop(0)

        color_switcher = {
            0: "#000000",  # Czarny
            1: "#FF0000",  # Czerwony
            2: "#00FF00",  # Zielony
            3: "#0000FF",  # Niebieski
            4: "#FFFF00",  # Żółty
            5: "#FF00FF",  # Fioletowy
        }

        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.enemy[-1][0] * row_h + self.enemy_level * 5
        y1 = self.enemy[-1][1] * col_w + self.enemy_level * 5
        x2 = x1 + row_h + self.enemy_level * 5
        y2 = y1 + col_w + self.enemy_level * 5
        self.enemy_size[0] = x1, y1
        self.enemy_size[1] = x2, y2
        self.enemy_objects.append(
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill=color_switcher.get(self.enemy_level), outline=RED_COLOR,
            )
        )

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def update_snake(self, key):
        # Check if it hit the wall or its own body
        tail = self.snake[0]
        head = self.snake[-1]
        if tail != self.old_apple_cell:
            self.snake.pop(0)
        if key == "Left":
            self.snake.append((head[0] - 1, head[1]))
        elif key == "Right":
            self.snake.append((head[0] + 1, head[1]))
        elif key == "Up":
            self.snake.append((head[0], head[1] - 1))
        elif key == "Down":
            self.snake.append((head[0], head[1] + 1))

        head = self.snake[-1]
        if (
                head[0] > cols - 1
                or head[0] < 0
                or head[1] > rows - 1
                or head[1] < 0
                or len(set(self.snake)) != len(self.snake)
        ):
            # Hit the wall / Hit on body
            self.crashed = True
        elif self.apple_cell == head:
            # Got the apple
            self.old_apple_cell = self.apple_cell
            self.canvas.delete(self.apple_obj)
            self.place_apple()
            self.display_snake()
        else:
            self.snake_heading = key
            self.display_snake()

    def update_enemy(self):
        score = len(self.snake)
        if score in (4, 6):
            self.enemy_level = 1
        elif score in (7, 8):
            self.enemy_level = 2
        elif score in (9, 11):
            self.enemy_level = 3
        elif score in (12, 14):
            self.enemy_level = 4
        elif score in (15, 17):
            self.enemy_level = 5

        if self.enemy_level in (1, 2):
            self.enemy_speed = 0.2
        elif self.enemy_level in (3, 4):
            self.enemy_speed = 0.4
        elif self.enemy_level == 5:
            self.enemy_speed = 0.7
        else:
            self.enemy_speed = 0

        if not self.crashed:
            snake_head = self.snake[-1]
            enemy_head = self.enemy[-1]

            dx = snake_head[0] - enemy_head[0]
            dy = snake_head[1] - enemy_head[1]

            if abs(dx) > abs(dy):
                if dx < 0:
                    self.enemy.append((enemy_head[0] - self.enemy_speed, enemy_head[1]))
                else:
                    self.enemy.append((enemy_head[0] + self.enemy_speed, enemy_head[1]))
            else:
                if dy < 0:
                    self.enemy.append((enemy_head[0], enemy_head[1] - self.enemy_speed))
                else:
                    self.enemy.append((enemy_head[0], enemy_head[1] + self.enemy_speed))
            self.enemy.pop(0)

        self.display_enemy()

    def check_if_key_valid(self, key):
        valid_keys = ["Up", "Down", "Left", "Right"]
        if key in valid_keys and self.forbidden_actions[self.snake_heading] != key:
            return True
        else:
            return False

    def mouse_input(self, event):
        self.play_again()

    def key_input(self, event):
        if not self.crashed:
            key_pressed = event.keysym
            # Check if the pressed key is a valid key
            if self.check_if_key_valid(key_pressed):
                # print(key_pressed)
                self.begin = True
                self.last_key = key_pressed

    def check_collision(self, snake, enemy_head, enemy_tail):
        # Snake coordinates
        snake_x = snake[0] * 50
        snake_y = snake[1] * 50

        # Enemy coordinates
        enemy_x1 = enemy_head[0]
        enemy_x2 = enemy_tail[0]
        enemy_y1 = enemy_head[1]
        enemy_y2 = enemy_tail[1]

        # Snake collision area
        snake_collision_area = (snake_x, snake_y, snake_x + 1, snake_y + 1)

        # Enemy collision area
        enemy_collision_area = (enemy_x1, enemy_y1, enemy_x2, enemy_y2)

        # Check if the collision areas overlap
        return self.overlap(snake_collision_area, enemy_collision_area)

    def overlap(self, rect1, rect2):
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2

        return not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4)


game_instance = SnakeAndApple()
game_instance.mainloop()
