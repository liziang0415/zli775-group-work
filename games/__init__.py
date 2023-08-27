from flask import Flask

from .gameDescription_bp import game_description_bp
from .home_bp import home_bp
from .games_bp import games_bp
from games.adapters.memory_repository import MemoryRepository, populate
import games.adapters.repository as repo


def create_app():
    app = Flask(__name__)
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)
    app.register_blueprint(home_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(game_description_bp)
    return app
