import pytest
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel import User, Game, Publisher, Genre, Review

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    user2 = repo.get_user('Dave')
    assert user2 == user and user2 is user


def test_repository_can_add_a_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(121, 'Game Title')
    previous_game_count = repo.get_number_of_game()
    repo.add_game(game)
    now_game_count = repo.get_number_of_game()

    assert previous_game_count + 1 == now_game_count


def test_repository_can_add_a_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    publisher = Publisher('Publisher Name')
    repo.add_publisher(publisher)

    publisher_fetched = repo.get_publisher_by_name('Publisher Name')
    assert publisher_fetched == publisher


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre('Action')
    repo.add_genre(genre)

    genre_get = repo.get_genres('Action')
    assert genre == genre_get


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    games = repo.get_games()

    review = Review(user, games[0], 4, "Good")
    repo.add_review(review)
    title = games[0].title

    reviews = repo.get_reviews_for_game(title)
    assert review in reviews


# Test retrieval functionalities

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    user2 = repo.get_user('Dave')
    assert user2 == user


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('NonExistentUser')
    assert user is None


def test_repository_can_retrieve_games_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(123,'Game Title')
    repo.add_game(game)

    games = repo.find_game_by_title('Game Title')
    assert game == games


# Test wishlist functionalities

def test_repository_can_add_to_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)
    games = repo.get_games()
    game = games[0]

    repo.add_to_wishlist('Dave', game)
    wishlist = repo.get_wishlist('Dave')

    assert game in wishlist


def test_repository_can_remove_from_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    games = repo.get_games()
    game = games[0]

    repo.add_to_wishlist('Dave', game)
    repo.remove_from_wishlist('Dave', game)
    wishlist = repo.get_wishlist('Dave')

    assert game not in wishlist

