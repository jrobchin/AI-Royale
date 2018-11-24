import random
import math
from ..engine.math import Vector

WIDTH = 512
HEIGHT = 256
MID_POINT = Vector(WIDTH/2, HEIGHT/2)
LEFT_MID_POINT = Vector(0, HEIGHT/2)
RIGHT_MID_POINT = Vector(WIDTH, HEIGHT/2)
BALL_SPEED = 4
PADDLE_SPEED = 4
PADDLE_HEIGHT = 50

class Ball:
    def __init__(self, pos, vel=None, speed=None, direction=None):
        self.pos = pos
        if vel is not None:
            self.vel = vel
        else:
            self.vel = Vector(r=speed, theta=direction)

    def update(self, lpaddle, rpaddle):
        # Vertical collision checks
        if self.pos.y < 0:
            self.vel.y = abs(self.vel.y)

        if self.pos.y > HEIGHT:
            self.vel.y = -abs(self.vel.y)

        # Horizontal collision checks
        if self.pos.x < 1:
            if self.pos.y < lpaddle.top() and self.pos.y > lpaddle.bottom():
                self.vel.x = abs(self.vel.x)
            else:
                self.pos = MID_POINT

        if self.pos.x > WIDTH - 1:
            if self.pos.y < rpaddle.top() and self.pos.y > rpaddle.bottom():
                self.vel.x = -abs(self.vel.x)
            else:
                self.pos = MID_POINT

        self.pos = self.pos.add(self.vel)

class Paddle:
    def __init__(self, pos):
        self.pos = pos
        self.height = PADDLE_HEIGHT
    
    def top(self):
        return self.pos.y + self.height

    def bottom(self):
        return self.pos.y - self.height

    def move(self, direction):
        if direction == -1 and self.top() < HEIGHT:
            self.pos.y += PADDLE_SPEED
        elif direction == 1 and self.bottom() > 0:
            self.pos.y -= PADDLE_SPEED
                            
class Pong:
    def __init__(self, lpaddle=None, rpaddle=None, ball=None):
        if lpaddle is None:
            self.lpaddle = Paddle(LEFT_MID_POINT)
        else:
            self.lpaddle = lpaddle

        if rpaddle is None:
            self.rpaddle = Paddle(RIGHT_MID_POINT)
        else:
            self.rpaddle = rpaddle

        if ball is None:
            self.ball = Ball(MID_POINT, speed=BALL_SPEED, direction=random.choice([math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]))
        else:
            self.ball = ball

    @staticmethod
    def from_state(state):
        lpaddle = Paddle(Vector(*state['lpaddle']))
        rpaddle = Paddle(Vector(*state['rpaddle']))
        ball = Ball(Vector(*state['ball']['pos']), Vector(x=state['ball']['vel'][0], y=state['ball']['vel'][1]))
        return Pong(lpaddle, rpaddle, ball)

    def next_state(self, events):
        self.event(events)
        self.update()

        state = {
            "lpaddle": self.lpaddle.pos.to_list(),
            "rpaddle": self.rpaddle.pos.to_list(),
            "ball": {
                "pos": self.ball.pos.to_list(),
                "vel": self.ball.vel.to_list(),
            }
        }
        
        return state

    def update(self):
        self.ball.update(self.lpaddle, self.rpaddle)

    def event(self, events):
        for player, e in events.items():
            if player == "lpaddle":
                if e == "UP":
                    self.lpaddle.move(1)
                elif e == "DOWN":
                    self.lpaddle.move(-1)
            elif player == "rpaddle":
                if e == "UP":
                    self.rpaddle.move(1)
                elif e == "DOWN":
                    self.rpaddle.move(-1)