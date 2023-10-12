import abc
from typing import List
from games.domainmodel.model import Game, Publisher, Genre

repo_instance = None


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_game(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_game(self, game_title):
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_wishlist(self, username, game):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_wishlist(self, username, game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_wishlist(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def is_in_wishlist(self, username, game_title):
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher_by_name(self, name: Publisher.publisher_name):
        raise NotImplementedError
