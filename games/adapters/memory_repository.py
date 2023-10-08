from sqlalchemy.orm import sessionmaker
from games.adapters.repository import AbstractRepository
from games.domainmodel import model
from games.domainmodel.model import Game, User
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from typing import List


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


def populate_to_db(filename, engine):
    # Create a new session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Read the games.csv file
    reader = GameFileCSVReader(filename)
    reader.read_csv_file()
    games = reader.dataset_of_games

    # First, add all unique publishers and genres to the session
    publishers_set = set()
    genres_set = set()

    for game in games:
        if game.publisher and game.publisher.publisher_name:
            publishers_set.add(game.publisher.publisher_name)

    # Add publishers to the session
    for publisher_name in publishers_set:
        if publisher_name:  # Ensure that the publisher_name is not None or empty
            print(f"Attempting to add publisher: {publisher_name}")  # Debug print
            publisher = session.query(model.Publisher).filter_by(publisher_name=publisher_name).first()
            if not publisher:
                session.add(model.Publisher(publisher_name=publisher_name))
            else:
                print(f"Publisher {publisher_name} already exists in the database.")  # Debug print
        else:
            print("Encountered an empty or None publisher name.")

            # Add genres to the session
    for genre_name in genres_set:
        genre = session.query(model.Genre).filter_by(name=genre_name).first()
        if not genre:
            session.add(model.Genre(genre_name=genre_name))

    # Commit publishers and genres first
    session.commit()

    # Now, add games to the session
    for game in games:
        if game.title:
            session.add(game)

    # Commit the session to save changes to the database
    session.commit()
    session.close()
