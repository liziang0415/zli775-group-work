import pytest
from games.services import get_all_games, get_filtered_games, find_game_by_title, get_filtered_and_sorted_games, \
    get_sorted_publisher_and_genres
from games.adapters.memory_repository import MemoryRepository, populate

repo = MemoryRepository()
populate(repo)


def test_get_all_games():
    games = get_all_games(repo)
    assert len(games) == repo.get_number_of_game()


def test_get_all_publisher():
    publishers, genres = get_sorted_publisher_and_genres(repo)
    assert len(publishers) == 798
    assert len(genres) == 24


def test_find_game_by_title():
    game = find_game_by_title(repo, '10 Second Ninja X')
    assert game is not None
    assert game.title == '10 Second Ninja X'


def test_get_filtered_games_by_genre():
    games = get_filtered_games(repo, genre='Action')
    assert len(games) == 380
    assert games[0].title == 'Call of Duty® 4: Modern Warfare®'


def test_get_filtered_games_by_publisher():
    games = get_filtered_games(repo, publisher='3P Studios')
    assert len(games) == 1
    assert games[0].title == 'From Dusk To Dawn'


def test_get_filtered_and_sorted_games():
    games, genres = get_filtered_and_sorted_games(repo, page=1, genre_filter='Action', sort_order='title')
    assert len(games) == 18
    assert games[0].title == '10 Second Ninja X'
    assert 'Action' in genres


def test_non_existing_search_key():
    games = get_filtered_games(repo, query='NonExistent')
    assert games == []
