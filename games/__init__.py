from flask import Flask
from .home_bp import home_bp
from .games_bp import games_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(games_bp)
    return app
