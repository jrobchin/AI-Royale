import os
from functools import wraps
import threading
import atexit

from flask import Flask, redirect, g, request, url_for, flash, render_template, make_response

GAME = 'pong'

def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.cookies.get("uid") is None:
            flash("You must set a username first.", category="error")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        REDIS_URL = "redis://:saturation389@localhost:6379/0",
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET', 'POST'])
    def index():
        uid = request.cookies.get('uid')

        game_keys = [[key.decode(), key.decode().split(':')[-1]] for key in rs.keys("game:{}:*".format(GAME))]
        if request.method == 'POST':
            uid = request.form.get('uid')
            if uid != "":
                uid_was_unique = rs.sadd('uids', uid)
                if uid_was_unique:
                    resp = make_response(redirect("/"))
                    resp.set_cookie('uid', uid)
                    return resp
            flash("That uid is taken or empty!")
            return render_template('index.html')
        return render_template('index.html', uid=uid)

    @app.route('/tutorial')
    @session_required
    def tutorial():
        return render_template('tutorial.html')

    @app.route('/create')
    def create():
        return render_template('code.html')

    # register extentions
    from app.ext import rs
    rs.init_app(app)

    # apply the blueprints to the app
    from app import game
    app.register_blueprint(game.bp)

    return app