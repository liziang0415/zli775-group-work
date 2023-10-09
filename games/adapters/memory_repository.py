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