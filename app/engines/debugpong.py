from graphics import *
import time
import random
import math
from pong import game

win = GraphWin("Pong", 512, 256)
pong = None

def main(state):
    while True:
        pong = game.Pong.from_state(state)
        # state = pong.next_state(state, {"lpaddle": random.choice(["UP", "DOWN"]), "rpaddle": random.choice(["UP", "DOWN"])})
        state = pong.next_state(state)
        draw(pong)
        time.sleep(0.03)
    win.close()

def draw(pong):
    global win
    win.delete("all")
    ball = Circle(Point(pong.ball.pos.x, pong.ball.pos.y), 5)
    lpaddle = Rectangle(Point(*pong.lpaddle.top().to_list()), Point(*pong.lpaddle.bottom().to_list()))
    rpaddle = Rectangle(Point(*pong.rpaddle.top().to_list()), Point(*pong.rpaddle.bottom().to_list()))
    ball.draw(win)
    lpaddle.draw(win)
    rpaddle.draw(win)

if __name__ == "__main__":
    state = game.INITIAL_STATE


    main(state)