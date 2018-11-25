import os
from functools import wraps
import threading
import atexit

from flask import Flask, redirect, g, request, url_for, flash

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

    @app.route('/')
    def index():
        return redirect('/game')

    # register extentions
    from app.ext import rs
    rs.init_app(app)

    # apply the blueprints to the app
    from app import game
    app.register_blueprint(game.bp)

    return app


def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.cookies.get("uid") is None:
            flash("You must set a username first.", category="error")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function