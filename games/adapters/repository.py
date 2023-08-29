import abc
from typing import List

from games.domainmodel.model import Game

repo_instance = None


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_game(self):
        raise NotImplementedError
