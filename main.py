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
        self.apple_image = ImageTk.PhotoImage(Image.open("images/apple.png"))
        self.bonus_image = ImageTk.PhotoImage(Image.open("images/bonus.png"))
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
        self.snake_head = []
        self.snake_head_image = ImageTk.PhotoImage(Image.open("images/snake-head.png"))
        self.snake_body_image = ImageTk.PhotoImage(Image.open("images/snake-body.png"))
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
        self.enemy_image_lvl_1 = ImageTk.PhotoImage(Image.open("images/enemy_lvl_1.png").resize((50, 50)))
        self.enemy_image_lvl_2 = ImageTk.PhotoImage(Image.open("images/enemy_lvl_2.png").resize((60, 60)))
        self.enemy_image_lvl_3 = ImageTk.PhotoImage(Image.open("images/enemy_lvl_3.png").resize((70, 70)))
        self.enemy_image_lvl_4 = ImageTk.PhotoImage(Image.open("images/enemy_lvl_4.png").resize((80, 80)))
        self.enemy_image_lvl_5 = ImageTk.PhotoImage(Image.open("images/enemy_lvl_5.png").resize((100, 100)))
        self.enemy_objects = []
        self.enemy_size = [(0, 0), (1, 1)]
        self.enemy_cell = []
        self.enemy_speed = 0
        self.enemy_level = 0
        self.enemy_status = ""

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.initialize_snake()
        self.place_apple()
        self.place_bonus()
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
        self.apple_obj = self.canvas.create_image(x1, y1, anchor=NW, image=self.apple_image)

    def place_bonus(self):
        unoccupied_cels = set(self.board) - set(self.snake) - set(self.apple_cell)
        self.bonus_cell = random.choice(list(unoccupied_cels))
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.bonus_cell[0] * row_h
        y1 = self.bonus_cell[1] * col_w
        self.bonus_obj = self.canvas.create_image(x1, y1, anchor=NW, image=self.bonus_image)

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
                if self.snake[i] == self.snake[-1]:
                    self.snake_head = self.canvas.create_image(x1, y1, anchor=NW, image=self.snake_head_image)
                else:
                    self.snake_objects.append(
                        self.canvas.create_image(
                            x1, y1, anchor=NW, image=self.snake_body_image
                        )
                    )
        else:
            # only update head
            head = self.snake[-1]
            cell = self.snake[-2]
            row_h = int(size_of_board / rows)
            col_w = int(size_of_board / cols)
            x1 = cell[0] * row_h
            y1 = cell[1] * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            if self.snake_head:
                self.canvas.delete(self.snake_head)
                # Create a new image for the head
            self.snake_head = self.canvas.create_image(
                head[0]* row_h, head[1]* col_w, anchor=NW, image=self.snake_head_image
            )
            self.snake_objects.append(
                self.canvas.create_image(
                    x1, y1, anchor=NW, image=self.snake_body_image
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
                    self.canvas.create_image(
                        x1, y1, anchor=NW, image=self.snake_body_image
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

        enemy_skin_switcher = {
            0: self.enemy_image_lvl_1,
            1: self.enemy_image_lvl_1,
            2: self.enemy_image_lvl_2,
            3: self.enemy_image_lvl_3,
            4: self.enemy_image_lvl_4,
            5: self.enemy_image_lvl_5,
        }

        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.enemy[-1][0] * row_h + self.enemy_level * 5
        y1 = self.enemy[-1][1] * col_w + self.enemy_level * 5
        x2 = x1 + row_h + self.enemy_level * 5
        y2 = y1 + col_w + self.enemy_level * 5
        self.enemy_size[0] = x1, y1
        self.enemy_size[1] = x2, y2
        self.enemy_objects.append(self.canvas.create_image(x1, y1, anchor=NW, image=enemy_skin_switcher[self.enemy_level]))
    def show_animation_of_bonus_collection(self, row, col):
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        # Changing the colour of the cell to blue
        self.explode_animation_objects=[]
        for i in range(rows):
            x1 = i * row_h
            y1 = col * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            self.explode_animation_objects.append(
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="#0000FF"
            ))
        for j in range(cols):
            x1 = row * row_h
            y1 = j * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            self.explode_animation_objects.append(
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="#0000FF"
            ))
        # Change of cell colour back to default after 500 milliseconds
        self.window.after(500, lambda: list(map(self.canvas.delete, self.explode_animation_objects)))


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
        image_pil = Image.open("images/snake-head.png")
        if key == "Left":
            self.snake.append((head[0] - 1, head[1]))
            image_pil = image_pil.rotate(-180)
            self.snake_head_image = ImageTk.PhotoImage(image_pil)
        elif key == "Right":
            self.snake.append((head[0] + 1, head[1]))
            image_pil = image_pil.rotate(0)
            self.snake_head_image = ImageTk.PhotoImage(image_pil)
        elif key == "Up":
            self.snake.append((head[0], head[1] - 1))
            image_pil = image_pil.rotate(90)
            self.snake_head_image = ImageTk.PhotoImage(image_pil)
        elif key == "Down":
            self.snake.append((head[0], head[1] + 1))
            image_pil = image_pil.rotate(-90)
            self.snake_head_image = ImageTk.PhotoImage(image_pil)

        head = self.snake[-1]
        if len(set(self.snake)) != len(self.snake):
            # Hit on body
            self.crashed = True
        elif head[0] > cols - 1:
            self.snake.append((0, head[1]))
            self.snake.pop(0)
            self.display_snake()
        elif head[0] < 0:
            self.snake.append((cols, head[1]))
            self.snake.pop(0)
            self.display_snake()
        elif head[1] > rows - 1:
            self.snake.append((head[0], 0))
            self.snake.pop(0)
            self.display_snake()
        elif head[1] < 0:
            self.snake.append((head[0], rows))
            self.snake.pop(0)
            self.display_snake()
        elif self.apple_cell == head:
            # Got the apple
            self.old_apple_cell = self.apple_cell
            self.canvas.delete(self.apple_obj)
            self.place_apple()
            self.display_snake()
        elif self.bonus_cell == head:
            #Got the bonus
            self.explode_bonus()
            self.freeze_enemy(3)
            self.canvas.delete(self.bonus_obj)
            self.place_bonus()
            self.display_snake()
        else:
            self.snake_heading = key
            self.display_snake()

    def update_enemy(self):
        score = len(self.snake)
        if self.enemy_status == "":
            if score in (4, 6):
                self.enemy_level = 1
            elif score in (7, 9):
                self.enemy_level = 2
            elif score in (10, 12):
                self.enemy_level = 3
            elif score in (13, 20):
                self.enemy_level = 4
            elif score in (13, 20):
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
        enemy_x1 = enemy_head[0]+1
        enemy_x2 = enemy_tail[0]-1
        enemy_y1 = enemy_head[1]+1
        enemy_y2 = enemy_tail[1]-1

        # Snake collision area
        snake_collision_area = (snake_x, snake_y, snake_x + 50, snake_y + 50)

        # Enemy collision area
        enemy_collision_area = (enemy_x1, enemy_y1, enemy_x2, enemy_y2)

        # Check if the collision areas overlap
        return self.overlap(snake_collision_area, enemy_collision_area)

    def overlap(self, rect1, rect2):
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2

        return not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4)

    def explode_bonus(self):
        bonus_row, bonus_col = self.bonus_cell
        apple_row, apple_col = self.apple_cell
        self.show_animation_of_bonus_collection(bonus_row, bonus_col)
        for col in range(cols):
            if apple_col == bonus_col:
                self.old_apple_cell = self.bonus_cell
                self.canvas.delete(self.apple_obj)
                self.place_apple()

        for row in range(rows):
            if apple_row == bonus_row:
                self.old_apple_cell = self.bonus_cell
                self.canvas.delete(self.apple_obj)
                self.place_apple()

    def freeze_enemy(self, time):
        #TODO improving the overlap of effects
        if time <= 0:
            self.enemy_status = ""
        else:
            self.enemy_status = "freeze"
            self.enemy_level = 0
            self.window.after(1000, self.freeze_enemy, time - 1)

game_instance = SnakeAndApple()
game_instance.mainloop()
