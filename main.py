from graphics import *
import time
import random
import math
from games.pong.game import Pong

PADDLE_WIDTH = 5

win = GraphWin("Pong", 512, 256)
pong = None

def main(state):
    while True:
        pong = Pong.from_state(state)
        state = pong.next_state({"lpaddle": random.choice(["UP", "DOWN"]), "rpaddle": random.choice(["UP", "DOWN"])})
        draw(pong)
        time.sleep(0.03)
    win.close()

def draw(pong):
    global win
    win.delete("all")
    ball = Circle(Point(pong.ball.pos.x, pong.ball.pos.y), 5)
    lpaddle = Rectangle(Point(pong.lpaddle.pos.x, pong.lpaddle.top()), Point(pong.lpaddle.pos.x+PADDLE_WIDTH, pong.lpaddle.bottom()))
    rpaddle = Rectangle(Point(pong.rpaddle.pos.x, pong.rpaddle.top()), Point(pong.rpaddle.pos.x-PADDLE_WIDTH, pong.rpaddle.bottom()))
    ball.draw(win)
    lpaddle.draw(win)
    rpaddle.draw(win)

if __name__ == "__main__":
    state = {
        'lpaddle': [0, 128], 
        'rpaddle': [512, 0], 
        'ball': {
            'pos': [256, 128], 
            'vel': [4, -2.356194490192345]
        }
    }


    main(state)