from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from bisect import insort_left
import os
from typing import List


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__game = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__game, game)

    def get_games(self) -> List[Game]:
        return self.__game

    def get_number_of_game(self):
        return len(self.__game)


def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    game_file_name = os.path.join(dir_name, "datareader/games.csv")
    reader = GameFileCSVReader(game_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)
