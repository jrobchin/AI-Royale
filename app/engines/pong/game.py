import random
from math import sqrt, sin, cos, atan, pi

from cerberus import Validator

class Vector:
    def __init__(self, x=None, y=None, r=None, theta=None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        elif r is not None and theta is not None:
            self.x = r * cos(theta)
            self.y = r * sin(theta)
        else:
            raise ValueError("Should use either 'x' and 'y' OR 'r' and 'theta'.")

    def __str__(self):
        return "<Vector x:{} y:{} r:{} theta:{}>".format(self.x, self.y, self.mag(), self.theta())
    
    def mag(self):
        return sqrt(self.x**2 + self.y**2)

    def theta(self):
        return atan(self.y/self.x)

    def add(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def to_list(self):
        return [self.x, self.y]

WIDTH = 512
HEIGHT = 256
MID_POINT = Vector(WIDTH/2, HEIGHT/2)
LEFT_MID_POINT = Vector(0, HEIGHT/2)
RIGHT_MID_POINT = Vector(WIDTH, HEIGHT/2)
BALL_SPEED = 20
PADDLE_SPEED = 7
PADDLE_HEIGHT = 35
PADDLE_WIDTH = 5
TL_LEFT_MID_POINT = Vector(0, HEIGHT/2 - PADDLE_HEIGHT)
TL_RIGHT_MID_POINT = Vector(WIDTH, HEIGHT/2 - PADDLE_HEIGHT)
MAX_PLAYERS = 2
INITIAL_STATE = {
    "lpaddle": [TL_LEFT_MID_POINT.x, TL_LEFT_MID_POINT.y],
    "rpaddle": [TL_RIGHT_MID_POINT.x, TL_RIGHT_MID_POINT.y],
    "ball": {
        "pos": [MID_POINT.x, MID_POINT.y],
        "vel": [BALL_SPEED, -BALL_SPEED/4]
    },
    "MAX_PLAYERS": MAX_PLAYERS,
    "ready": False
}

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
            if self.pos.y < lpaddle.top().y + 5 and self.pos.y > lpaddle.bottom().y - 5:
                self.vel.x = abs(self.vel.x)
            else:
                self.pos = MID_POINT

        if self.pos.x > WIDTH - 1:
            if self.pos.y < rpaddle.top().y + 5 and self.pos.y > rpaddle.bottom().y - 5:
                self.vel.x = -abs(self.vel.x)
            else:
                self.pos = MID_POINT

        self.pos = self.pos.add(self.vel)

class Paddle:
    def __init__(self, pos):
        self.pos = pos
        self.height = PADDLE_HEIGHT
    
    def top(self):
        return Vector(self.pos.x, self.pos.y + self.height)

    def bottom(self):
        return Vector(self.pos.x, self.pos.y - self.height)

    def move(self, direction):
        if direction == -1 and self.top().y < HEIGHT - PADDLE_HEIGHT:
            self.pos.y += PADDLE_SPEED
        elif direction == 1 and self.bottom().y > 0 - PADDLE_HEIGHT:
            self.pos.y -= PADDLE_SPEED
                            
class Pong:
    def __init__(self, lpaddle=None, rpaddle=None, ball=None):
        if lpaddle is None:
            self.lpaddle = Paddle(TL_LEFT_MID_POINT)
        else:
            self.lpaddle = lpaddle

        if rpaddle is None:
            self.rpaddle = Paddle(TL_RIGHT_MID_POINT)
        else:
            self.rpaddle = rpaddle

        if ball is None:
            self.ball = Ball(MID_POINT, speed=BALL_SPEED, direction=random.choice([pi/4, 3*pi/4, 5*pi/4, 7*pi/4]))
        else:
            self.ball = ball

    @staticmethod
    def from_state(state):
        lpaddle = Paddle(Vector(*state['lpaddle']))
        rpaddle = Paddle(Vector(*state['rpaddle']))
        ball = Ball(Vector(*state['ball']['pos']), Vector(x=state['ball']['vel'][0], y=state['ball']['vel'][1]))
        return Pong(lpaddle, rpaddle, ball)

    def next_state(self, state, events=None):
        if events is not None:
            self.event(events)
        self.update()

        state["lpaddle"] = self.lpaddle.pos.to_list()
        state["rpaddle"] = self.rpaddle.pos.to_list()
        state["ball"]["pos"] = self.ball.pos.to_list()
        state["ball"]["vel"] = self.ball.vel.to_list()
        
        return state

    def update(self):
        self.ball.update(self.lpaddle, self.rpaddle)

    def event(self, events):
        for player, e in events.items():
            if player == "lpaddle":
                if e == "DOWN":
                    self.lpaddle.move(1)
                elif e == "UP":
                    self.lpaddle.move(-1)
            elif player == "rpaddle":
                if e == "DOWN":
                    self.rpaddle.move(1)
                elif e == "UP":
                    self.rpaddle.move(-1)