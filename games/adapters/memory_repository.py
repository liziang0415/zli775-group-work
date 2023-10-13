from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, Publisher, Genre, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from bisect import insort_left
import os
from typing import List
from games.services import NameNotUniqueException


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__game = list()
        self.__users = set()
        self.__reviews = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__game, game)

    def add_publisher(self, publisher: Publisher):
        return None

    def add_genre(self, genre: Genre):
        return None

    def get_games(self) -> List[Game]:
        return self.__game

    def get_number_of_game(self):
        return len(self.__game)

    def add_user(self, user: User):
        existing_user = self.get_user(user.username)
        if existing_user:
            raise NameNotUniqueException(f"Username {user.username} already exists!")
        user.wishlist = Wishlist(user)  # Initialize wishlist for the user
        self.__users.add(user)

    def get_user(self, username):
        for i in self.__users:
            if i.username.lower() == username.lower():
                return i

    def add_review(self, review):
        game = review.game
        user = review.user
        game.add_review(review)
        user.add_review(review)
        self.__reviews.append(review)

    def get_reviews_for_game(self, game_title):
        return [review for review in self.__reviews if review.game.title == game_title]

    def add_to_wishlist(self, username, game):
        user = self.get_user(username)
        if user:
            user.wishlist.add_game(game)

    def remove_from_wishlist(self, username, game):
        user = self.get_user(username)
        if user:
            user.wishlist.remove_game(game)

    def get_wishlist(self, username):
        user = self.get_user(username)
        print(user)
        if user and user.wishlist.list_of_games():
            return user.wishlist.list_of_games()
        return []

    def is_in_wishlist(self, username, game):
        user = self.get_user(username)
        if user:
            listgame = user.wishlist.list_of_games()
            return game in listgame
        return False

    def get_publisher_by_name(self, name: Publisher.publisher_name):
        return None


def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    game_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(game_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)
