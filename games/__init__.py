from flask import Flask
from sqlalchemy.orm import sessionmaker

from .adapters import orm
from .gameDescription_bp import game_description_bp
from .home_bp import home_bp
from .games_bp import games_bp
from.search_bp import search_bp
from.login_bp import login_bp
from.user_profile_bp import user_profile_bp
from.wishlist_bp import wishlist_bp
from games.adapters.memory_repository import MemoryRepository, populate_to_db
import games.adapters.repository as repo
from games.adapters.orm import engine, games_table


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dh13828808842',
        SESSION_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SECURE=True,
    )
    if test_config is not None:
        app.config.from_mapping(test_config)

    Session = sessionmaker(bind=engine)
    orm.metadata.create_all(orm.engine)
    orm.map_model_to_tables()
    repo.repo_instance = MemoryRepository(Session)
    populate_to_db("games/adapters/data/games.csv")

    app.register_blueprint(home_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(game_description_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')

    return app