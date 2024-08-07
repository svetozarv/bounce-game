from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas, paddle,  color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_puddle(pos):
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

    def hit_puddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                return True
            return False


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.window_is_active = False
        self.canvas.bind_all('<Button-1>', self.make_window_active)

    def make_window_active(self, event):
        self.window_is_active = True

    def turn_left(self, event):
        self.x = -2

    def turn_right(self, event):
        self.x = 2

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

def retry(canvas, ball, paddle):
    ball.hit_bottom = False
    canvas.move(ball.id, 245, 100)
    canvas.move(paddle.id, 200, 300)

tk = Tk()
tk.title('Bounce!')
tk.resizable(False, False)
tk.wm_attributes('-topmost', 1)

canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
# score_counter = canvas.create_text(480, 30, text=f'{score}')
tk.update()

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')


while True:
    if paddle.window_is_active:
        if not ball.hit_bottom:
            ball.draw()
            paddle.draw()
        else:
            canvas.create_text(250, 250, text='Game Over', font=('Calibri', 40))
            # canvas.bind_all('<KeyPress-Right>', retry(canvas, ball, paddle))            
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
