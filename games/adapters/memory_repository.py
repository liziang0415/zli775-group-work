<<<<<<< Updated upstream
from flask_sqlalchemy.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from games.adapters.repository import AbstractRepository
from games.domainmodel import model
from games.domainmodel.model import Game, User
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from typing import List

DATABASE_URL = "sqlite:///games.db"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
class MemoryRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def add_game(self, game: Game):
        if isinstance(game, Game):
            with self._session_factory() as session:
                session.add(game)
                session.commit()

    def get_games(self) -> List[Game]:
        with self._session_factory() as session:
            return session.query(model.Game).all()

    def get_number_of_game(self):
        with self._session_factory() as session:
            return session.query(model.Game).count()

    def get_game_by_title(self, name):
        with self._session_factory() as session:
            return session.query(model.Game).filter_by(title=name).first()

    def add_user(self, user: User):
        if isinstance(user, User):
            with self._session_factory() as session:
                session.add(user)
                session.commit()

    def get_user(self, username):
        with self._session_factory() as session:
            return session.query(model.User).filter_by(username=username.lower()).first()

    def add_review(self, review):
        with self._session_factory() as session:
            session.add(review)
            session.commit()

    def get_reviews_for_game(self, game_title):
        with self._session_factory() as session:
            return session.query(model.Review).filter_by(game_title=game_title).all()

    def add_to_wishlist(self, username, game_title):
        with self._session_factory() as session:
            user = session.query(model.User).filter_by(username=username).first()
            game = session.query(model.Game).filter_by(title=game_title).first()
            if user and game:
                user.favourite_games.append(game)
                session.commit()

    def remove_from_wishlist(self, username, game_title):
        with self._session_factory() as session:
            user = session.query(model.User).filter_by(username=username).first()
            game = session.query(model.Game).filter_by(title=game_title).first()
            if user and game:
                user.favourite_games.remove(game)
                session.commit()

    def get_wishlist(self, username):
        with self._session_factory() as session:
            user = session.query(model.User).filter_by(username=username).first()
            if user:
                return user.favourite_games
            return []

    def is_in_wishlist(self, username, game_title):
        with self._session_factory() as session:
            user = session.query(model.User).filter_by(username=username).first()
            game = session.query(model.Game).filter_by(title=game_title).first()
            if user and game:
                return game in user.favourite_games
            return False


def populate_to_db(filename):
    session = Session()

    game_reader = GameFileCSVReader(filename)
    game_reader.read_csv_file()

    for publisher in game_reader.dataset_of_publishers:
        session.add(publisher)

    for genre in game_reader.dataset_of_genres:
        session.add(genre)

    for game in game_reader.dataset_of_games:
        session.add(game)
    session.commit()
    session.close()
=======
import os
from typing import List, Type

from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, scoped_session

from .datareader import GameFileCSVReader
from .orm import metadata, Game, Publisher, Genre
from games.services import NameNotUniqueException
from .repository import AbstractRepository
from ..domainmodel import User, Game


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class MemoryRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.add(game)
            scm.commit()

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_games(self) -> list[Game]:
        return self._session_cm.session.query(Game).all()

    def get_number_of_game(self):
        return self._session_cm.session.query(Game).count()


    def add_user(self, user: User):
        with self._session_cm as scm:
            existing_user = scm.session.query(User).filter_by(username=user.username).first()
            if existing_user:
                raise NameNotUniqueException(f"Username {user.username} already exists!")
            scm.session.add(user)
            scm.commit()

    def get_user(self, username):
        users = self._session_cm.session.query(User).all()
        for user in users:
            if user.username == username:
                return user

    def add_review(self, review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews_for_game(self, game_title):
        game = self._session_cm.session.query(Game).filter_by(title=game_title).first()
        if game:
            return game.reviews
        return []

    def add_to_wishlist(self, username, game):
        with self._session_cm as scm:
            user = self.get_user(username)
            if user:
                user.add_favourite_game(game)
                scm.commit()

    def remove_from_wishlist(self, username, game):
        with self._session_cm as scm:
            user = self.get_user(username)
            if user:
                user.remove_favourite_game(game)
                scm.commit()

    def get_wishlist(self, username):
        user = self.get_user(username)
        if user:
            return user.favourite_games

    def is_in_wishlist(self, username, game):
        user = self.get_user(username)
        if user:
            return game in user.favourite_games
        return False

    def get_publisher_by_name(self, publisher_name):
        try:
            return self._session_cm.session.query(Publisher).filter_by(publisher_name=publisher_name).one()
        except NoResultFound:
            return None


def populate(repo):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    game_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(game_file_name)
    reader.read_csv_file()
    print(reader.get_unique_publishers_count())

    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)
        repo.commit()

    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)
        repo.commit()

    for game in reader.dataset_of_games:
        repo.add_game(game)
        repo.commit()
>>>>>>> Stashed changes
