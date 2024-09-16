from tkinter import *
import random

GAME_WIDTH = 725
GAME_HEIGHT = 725
SPEED = 70
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#C0FF40"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#400080"
PAD_X = 50  
PAD_BOTTOM = 50

class Snake:
    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append((0,0))
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, snake_body): 

        snake_body_set = set(snake_body)
        while True:
            x = random.randint(0 , (GAME_WIDTH//SPACE_SIZE)-1)*SPACE_SIZE
            y = random.randint(0 , (GAME_HEIGHT//SPACE_SIZE)-1)*SPACE_SIZE
            self.coordinates = (x,y)
            if (x,y) not in snake_body_set:
                break
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake,food):

    global paused
    if paused:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    new_head = (x,y)
    snake.coordinates.insert(0, new_head)
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food(snake.coordinates)

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
    
def check_collision(snake):

    x,y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
    
def restart_game():

    global snake, food, score, direction

    canvas.delete(ALL)
    snake = Snake()
    food = Food(snake.coordinates)
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)

def toggle_pause():

    global paused
    paused = not paused
    if paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        next_turn(snake, food)

window = Tk()
window.title("Snake Game")
window.resizable(False,False)

score = 0
direction = 'down'
paused = False

label=Label(window, text="Score:{}".format(score), font=('consolas' , 35))
label.place(x=(GAME_WIDTH + 2 * PAD_X) // 2 - 100, y=10)
canvas=Canvas(window, bg = BG_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.place(x=PAD_X, y=75)

window.update()
window_width = GAME_WIDTH + 2 * PAD_X
window_height = GAME_HEIGHT + PAD_BOTTOM + 100
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

key_directions = {'<Left>': 'left', '<Right>': 'right','<Up>': 'up','<Down>': 'down',
                  'w': 'up','a': 'left','s': 'down','d': 'right'}

for key, direction in key_directions.items():
    window.bind(key, lambda event, dir=direction: change_direction(dir))

snake = Snake()
food = Food(snake.coordinates)

next_turn(snake, food)

restart_button = Button(window, text="Restart", command=restart_game, font=('consolas', 20), bg = 'black', fg = 'white')
restart_button.place(x=0, y=0)

pause_button = Button(window, text="Pause", command=toggle_pause, font=('consolas', 20), bg = 'black', fg = 'white')
pause_button.place(x=715, y=0)

window.mainloop()