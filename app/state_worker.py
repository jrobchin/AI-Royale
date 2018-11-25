import json
import time
import requests
import redis
from engines.pong import game as pong
import random

GAME = 'pong'
REMOTE = True

def format_for_bots(state, paddle):
    """
    paddle, ballPos, ballVel
    """
    s = {}
    s['paddle'] = [state[paddle][0], state[paddle][1] + pong.PADDLE_HEIGHT]
    s['ballPos'] = state['ball']['pos']
    s['ballVel'] = state['ball']['vel']

    return s

if __name__ == "__main__":
    rs = redis.Redis(host='localhost', port=6379, db=0, password='saturation389')

    while True:
        for key in rs.keys("game:{}:*".format(GAME)):
            print(key)

            # get game state
            state = json.loads(rs.get(key).decode())
            if not state.get('start'):
                continue
            
            bots = state['bots']
            events = {}
            for role, attrs in bots.items():
                state_for_bot = format_for_bots(state, role)
                if REMOTE:
                    res = requests.post(attrs['url'], data=state_for_bot).json()
                    move = res['event']
                    if move == -1:
                        events['lpaddle'] = "DOWN"
                        events['rpaddle'] = "DOWN"
                    elif move == 1:
                        events['lpaddle'] = "UP"
                        events['rpaddle'] = "UP"
                    break
                else:
                    if state_for_bot['ballPos'][1] > state_for_bot['paddle'][1] == -1:
                        events['lpaddle'] = "DOWN"
                        events['rpaddle'] = "DOWN"
                    elif state_for_bot['ballPos'][1] < state_for_bot['paddle'][1] == 1:
                        events['lpaddle'] = "UP"
                        events['rpaddle'] = "UP"
                    break
                    time.sleep(0.2)

            # calculate next state
            state = pong.Pong.from_state(state).next_state(state, events)

            # set state
            rs.set(key, json.dumps(state))