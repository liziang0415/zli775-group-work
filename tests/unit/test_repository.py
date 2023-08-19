import pytest
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game, Genre, Publisher


@pytest.fixture
def repo():
    repo = MemoryRepository()
    game1 = Game(1, "Game 1")
    game2 = Game(2, "Game 2")
    repo.add_game(game1)
    repo.add_game(game2)
    return repo


def test_add_game(repo):
    new_game = Game(3, "Game 3")
    repo.add_game(new_game)
    assert new_game in repo.get_games()


def test_retrieve_game(repo):
    game = repo.get_games()[0]
    assert game.game_id == 1
    assert game.title == "Game 1"


def test_retrieve_number_of_games(repo):
    assert repo.get_number_of_game() == 2


def test_unique_genres(repo):
    genre1 = Genre("Action")
    genre2 = Genre("Adventure")
    game = repo.get_games()[0]
    game.add_genre(genre1)
    game.add_genre(genre2)
    assert len(set([genre for game in repo.get_games() for genre in game.genres])) == 2


def test_add_new_genre(repo):
    genre = Genre("RPG")
    game = repo.get_games()[0]
    initial_genre_count = len(game.genres)
    game.add_genre(genre)
    assert len(game.genres) == initial_genre_count + 1


def test_search_games_by_title(repo):
    search_result = [game for game in repo.get_games() if game.title == "Game 1"]
    assert len(search_result) == 1
    assert search_result[0].game_id == 1


def test_search_games_by_publisher(repo):
    publisher = Publisher("Publisher A")
    game = repo.get_games()[0]
    game.publisher = publisher
    search_result = [game for game in repo.get_games() if game.publisher == publisher]
    assert len(search_result) == 1
    assert search_result[0].game_id == 1


def test_search_games_by_genre(repo):
    genre = Genre("Action")
    game = repo.get_games()[0]
    game.add_genre(genre)
    search_result = [game for game in repo.get_games() if genre in game.genres]
    assert len(search_result) == 1
    assert search_result[0].game_id == 1
