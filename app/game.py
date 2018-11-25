import os
import json
import random
import base64

from app import session_required

from flask import Blueprint, jsonify, request, render_template, make_response, flash, redirect
from app.ext import rs
from app.utils import redis_game_key

from app.engines.pong import game as pong

import requests

UIDS = []

GAME = 'pong'
def safe_check(check_string):
    UNSAFE_CHARS = [';', '/', '?', ':', '@', 
                    '=', '&', '"', '<', '>', 
                    '#', '%', '{', '}', '|', 
                    '\\', '^', '~', '[', ']', 
                    '`']
    for c in UNSAFE_CHARS:
        if c in check_string:
            return False
    return True

def format_for_bots(state, paddle):
    """
    paddle, ballPos, ballVel
    """
    s = {}
    s['paddle'] = [state[paddle][0], state[paddle][1] + pong.PADDLE_HEIGHT]
    s['ballPos'] = state['ball']['pos']
    s['ballVel'] = state['ball']['vel']

    return s


bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/', methods=['GET', 'POST'])
@session_required
def game_index():
    uid = request.cookies.get('uid')

    games = []
    game_keys = [[key.decode(), key.decode().split(':')[-1]] for key in rs.keys("game:{}:*".format(GAME))]
    for key in game_keys:
        game = {'gid': key[1]}

        state = json.loads(rs.get(key[0]).decode())

        game['owner'] = state['owner']
        game['elo'] = random.randint(100, 3000)
        game['n_players'] = len(state['players'])
        if game['n_players'] < 2:
            game['button'] = "Join"
        else:
            game['button'] = "Watch"

        games.append(game)

    if request.method == 'POST':
        uid = request.form.get('uid')
        if uid != "":
            uid_was_unique = rs.sadd('uids', uid)
            if uid_was_unique:
                resp = make_response(redirect("/game"))
                resp.set_cookie('uid', uid)
                return resp
        flash("That uid is taken or empty!")
    return render_template('leaderboard.html', games=games, uid=uid)

@bp.route('/create', methods=['GET', 'POST'])
@session_required
def create_game():
    """
    ARGS:
        computer (boolean): should we provide a computer.
    
    GET:
        ret: create game page.
    
    POST:
        body:
            bot_url
            bot_role
    """

    if request.method == 'GET':
        return render_template('creategame.html')
    elif request.method == 'POST':
        # parse args
        with_computer = request.args.get('computer')

        # parse form
        bot_url = request.form['bot_url']
        bot_role = request.form['bot_role'] # role in game (eg. which pong paddle)

        # generate new game id
        gid = base64.b64encode(os.urandom(32))[:8].decode()
        while not safe_check(gid):
            gid = base64.b64encode(os.urandom(32))[:8].decode()
        redis_key = redis_game_key(gid, GAME)
        
        # set initial game state
        state = pong.INITIAL_STATE

        # add players
        uid = request.cookies.get('uid') 
        state['owner'] = uid

        # add bot to game state
        state['bots'] = {}
        if with_computer:
            state['players'] = [
                'computer',
                uid
            ]
            state['bots'] = {
                'lpaddle': {
                    "username": 'computer',
                    "url": 'https://json.lib.id/zhuda-bot-builder@dev/',
                },
                'rpaddle': {
                    "username": uid,
                    "url": bot_url,
                }
            }
            state['start'] = True
            rs.set(redis_key, json.dumps(state))
            return redirect('/game/play/{}'.format(gid))

        state['players'] = [
            uid
        ]
        state['bots'] = {
            bot_role: {
                "username": uid,
                "url": bot_url,
            }
        }

        rs.set(redis_key, json.dumps(state))
        return redirect('/game/lobby/{}'.format(gid))

@bp.route('/join/<gid>', methods=['GET', 'POST'])
@session_required
def join_game(gid):
    """
    GET:
        ret: join game page.
    
    POST:
        form:
            
    """
    
    if request.method == 'GET':
        uid = request.cookies.get('uid')

        # get game state
        redis_key = redis_game_key(gid, GAME)
        state = json.loads(rs.get(redis_key).decode())

        if len(state['players']) > 1:
            return redirect("/game/play/{}".format(gid))
        # if len(state['players']) >= state['MAX_PLAYERS'] and uid not in state['players']:
        #     flash("Cannot join game, already full.")
        #     return redirect('/game')

        # if uid in state['players']:
        #     return redirect('/game/lobby/{}'.format(gid))
        # else:
        return render_template('join.html', gid=gid)
    elif request.method == 'POST':
        # parse form
        bot_url = request.form['bot_url']
        bot_role = request.form['bot_role'] # role in game (eg. which pong paddle)

        # get user id
        uid = request.cookies.get('uid')

        # get game state
        redis_key = redis_game_key(gid, GAME)
        state = json.loads(rs.get(redis_key).decode())
        if len(state['players']) >= state['MAX_PLAYERS'] and uid not in state['players']:
            flash("Cannot join game, already full.")
            return redirect('/game/join/{}'.format(gid))

        state['players'].append(uid)

        # add joined player to state
        state['bots'][bot_role] = {"username": uid, "url": bot_url}
        if len(state['players']) > 1:
            state['ready'] = True
        rs.set(redis_key, json.dumps(state))

        return redirect('/game/start/{}'.format(gid))

@bp.route('/lobby/<gid>')
@session_required
def lobby_game(gid):
    # get game state
    redis_key = redis_game_key(gid, GAME)
    state = json.loads(rs.get(redis_key).decode())    

    uid = request.cookies.get('uid')
    players = state['players']
    ready = state['ready']

    return render_template('lobby.html', players=players, player_count=len(players), gid=gid, ready=ready)

@bp.route('/start/<gid>')
@session_required
def start_game(gid):
    # get game state
    redis_key = redis_game_key(gid, GAME)
    state = json.loads(rs.get(redis_key).decode())

    state['start'] = True
    rs.set(redis_key, json.dumps(state))
    
    if request.args.get('json'):
        return jsonify({"gid": gid, "state": state})
    return redirect('/game/play/{}'.format(gid))

@bp.route('/state/<gid>')
def get_state(gid):
    redis_key = redis_game_key(gid, GAME)
    state = json.loads(rs.get(redis_key).decode())
    return jsonify(state)

@bp.route('/play/<gid>')
@session_required
def show_game(gid):
    state_only = request.args.get("state")
    if state_only:
        # get game state
        redis_key = redis_game_key(gid, GAME)
        state = json.loads(rs.get(redis_key).decode())
        return jsonify(state)
    else:
        # get game state
        redis_key = redis_game_key(gid, GAME)
        state = json.loads(rs.get(redis_key).decode())
        return render_template('watchgame.html', gid=gid, player1=state['players'][0], player2=state['players'][1])

@bp.route('/next-states')
def next_states():
    for key in rs.keys("game:{}:*".format(GAME)):
        # get game state
        state = json.loads(rs.get(key).decode())
        
        bots = state['bots']
        events = {}
        for role, attrs in bots.items():
            state_for_bot = format_for_bots(state, role)
            res = requests.post(attrs['url'], data=state_for_bot).json()
            move = res['event']
            if move == -1:
                events[role] = "DOWN"
            elif move == 1:
                events[role] = "UP"

        # calculate next state
        state = pong.Pong.from_state(state).next_state(state, events)

        # set state
        rs.set(key, json.dumps(state))
    return "Did it!"