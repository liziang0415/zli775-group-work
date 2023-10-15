import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from .adapters import memory_repository
from .gameDescription_bp import game_description_bp
from .home_bp import home_bp
from .games_bp import games_bp
from .search_bp import search_bp
from .login_bp import login_bp
from .user_profile_bp import user_profile_bp
from .wishlist_bp import wishlist_bp
from .adapters.database_repository import SqlAlchemyRepository, populate
from .adapters.orm import metadata, map_model_to_tables
import games.adapters.repository as repo

DATABASE_URI = 'sqlite:///games.db'  # SQLite database URI


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    if test_config is not None:
        app.config.from_mapping(test_config)
    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = memory_repository.MemoryRepository()
        populate(repo.repo_instance)
    elif app.config['REPOSITORY'] == 'database':
        database_engine = create_engine(DATABASE_URI)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = SqlAlchemyRepository(session_factory)
        clear_mappers()
        map_model_to_tables()
        if not os.path.isfile('games.db'):
            metadata.create_all(database_engine)
            populate(repo.repo_instance)

    app.register_blueprint(home_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(game_description_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')
    return app