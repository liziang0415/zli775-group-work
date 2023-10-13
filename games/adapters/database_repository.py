import os
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from .datareader import GameFileCSVReader
from .orm import Publisher, Genre
from games.services import NameNotUniqueException
from .repository import AbstractRepository
from ..domainmodel import User, Game, Wishlist


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


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
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
                wishlist = user.wishlist
                if not wishlist:
                    wishlist = Wishlist(user)
                    user.wishlist = wishlist
                    scm.session.add(wishlist)
                wishlist.add_game(game)
                scm.commit()

    def remove_from_wishlist(self, username, game):
        with self._session_cm as scm:
            user = self.get_user(username)
            if user:
                wishlist = user.wishlist
                if wishlist:
                    wishlist.remove_game(game)
                    scm.commit()

    def get_wishlist(self, username):
        user = self.get_user(username)
        if user and user.wishlist:
            return user.wishlist.list_of_games()
        return []

    def is_in_wishlist(self, username, game):
        user = self.get_user(username)
        if user and user.wishlist:
            return game in user.wishlist.list_of_games()
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

    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)

    for game in reader.dataset_of_games:
        repo.add_game(game)

