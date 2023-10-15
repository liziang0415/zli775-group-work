import pytest
from sqlalchemy.exc import IntegrityError
from games.domainmodel.model import Game, Publisher, User, Review, Genre, Wishlist


def insert_publisher(empty_session, publisher_name):
    empty_session.execute('INSERT INTO publishers (publisher_name) VALUES (:publisher_name)',
                          {'publisher_name': publisher_name})


def insert_game(empty_session, title, publisher_name):
    empty_session.execute(
        'INSERT INTO games (title, publisher_name) VALUES (:title, :publisher_name)',
        {'title': title, 'publisher_name': publisher_name}
    )
    row = empty_session.execute('SELECT id from games where title = :title',
                                {'title': title}).fetchone()
    return row[0]



def test_loading_of_publisher(empty_session):
    insert_publisher(empty_session, "EA Sports")
    publishers = empty_session.query(Publisher).all()
    assert len(publishers) == 1
    assert publishers[0].publisher_name == "EA Sports"


def test_saving_of_publisher(empty_session):
    publisher = Publisher("EA Sports")
    empty_session.add(publisher)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT publisher_name FROM publishers'))
    assert rows == [("EA Sports",)]


def test_loading_of_game(empty_session):
    insert_publisher(empty_session, "EA Sports")
    insert_game(empty_session, "FIFA 23", "EA Sports")

    games = empty_session.query(Game).all()
    assert len(games) == 1
    assert games[0].title == "FIFA 23"
    assert games[0].publisher.publisher_name == "EA Sports"


def test_saving_of_game(empty_session):
    publisher = Publisher("EA Sports")
    game = Game(123, "FIFA 23")
    game.publisher = publisher
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, publisher_name FROM games'))
    assert rows == [("FIFA 23", "EA Sports")]


def test_game_and_publisher_relationship(empty_session):
    publisher = Publisher("EA Sports")
    game1 = Game(123, "FIFA 23")
    game2 = Game(246, "Madden NFL 23")
    game1.publisher = publisher
    game2.publisher = publisher
    empty_session.add_all([game1, game2])
    empty_session.commit()

    games = empty_session.query(Game).all()
    assert len(games) == 2
    for game in games:
        assert game.publisher.publisher_name == "EA Sports"


def test_loading_of_user(empty_session):
    empty_session.execute('INSERT INTO users (username, password) VALUES ("JohnDoe", "pass123")')
    users = empty_session.query(User).all()
    assert len(users) == 1
    assert users[0].username == "JohnDoe"


# User Tests
def test_loading_of_user(empty_session):
    empty_session.execute('INSERT INTO users (username, password) VALUES ("JohnDoe", "pass123")')
    users = empty_session.query(User).all()
    assert len(users) == 1
    assert users[0].username == "JohnDoe"


def test_saving_of_user(empty_session):
    user = User("johndoe", "pass123")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username FROM users'))
    assert rows == [("johndoe",)]


# Review Tests
def test_loading_of_review(empty_session):
    game_id = insert_game(empty_session, "FIFA 23", "EA Sports")
    empty_session.execute('INSERT INTO reviews (game_id, comment, rating) VALUES (:game_id, "Great game!", 5)',
                          {'game_id': game_id})
    reviews = empty_session.query(Review).all()
    assert len(reviews) == 1
    assert reviews[0].comment == "Great game!"
    assert reviews[0].rating == 5


def test_saving_of_review(empty_session):
    user = User("john", "Dh123123")
    game = Game(123, "FIFA 23")
    review = Review(user, game, 5, "Great game!", )
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT comment, rating FROM reviews'))
    assert rows == [("Great game!", 5)]


# Genre Tests
def test_loading_of_genre(empty_session):
    empty_session.execute('INSERT INTO genres (genre_name) VALUES ("Sports")')
    genres = empty_session.query(Genre).all()
    assert len(genres) == 1
    assert genres[0].genre_name == "Sports"


def test_saving_of_genre(empty_session):
    genre = Genre("Sports")
    empty_session.add(genre)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT genre_name FROM genres'))
    assert rows == [("Sports",)]


# Wishlist Tests

def test_loading_of_wishlist(empty_session):
    user = User("JohnDoe", "pass123")
    publisher = Publisher("EA Sports")
    game = Game(123,"FIFA 23")

    wishlist = Wishlist(user)
    wishlist.list_of_games().append(game)
    user.wishlist = wishlist

    empty_session.add(user)
    empty_session.commit()

    users_in_db = empty_session.query(User).all()
    user_in_db = next((u for u in users_in_db if u.username.lower() == "JohnDoe".lower()), None)
    assert user_in_db is not None
    assert "FIFA 23" in [game._Game__game_title for game in user_in_db._User__wishlist._Wishlist__list_of_games]


# Wishlist Tests

def test_saving_of_wishlist(empty_session):
    user = User("JohnDoe", "pass123")
    game = Game(123, "FIFA 23")

    wishlist = Wishlist(user)
    wishlist.list_of_games().append(game)
    user.wishlist = wishlist

    empty_session.add(user)
    empty_session.commit()

    users_in_db = empty_session.query(User).all()
    user_in_db = next((u for u in users_in_db if u.username.lower() == "JohnDoe".lower()), None)
    assert user_in_db is not None
    assert "FIFA 23" in [game.title for game in user_in_db.wishlist.list_of_games()]


def test_wishlist_relationship(empty_session):
    user = User("JohnDoe", "pass123")
    game1 = Game(123, "FIFA 23")
    game2 = Game(124, "Madden NFL 23")

    wishlist = Wishlist(user)
    wishlist.list_of_games().extend([game1, game2])
    user.wishlist = wishlist

    empty_session.add(user)
    empty_session.commit()

    users_in_db = empty_session.query(User).all()
    user_in_db = next((u for u in users_in_db if u.username.lower() == "JohnDoe".lower()), None)
    assert user_in_db is not None
    games_in_wishlist = [game.title for game in user_in_db.wishlist.list_of_games()]
    assert "FIFA 23" in games_in_wishlist
    assert "Madden NFL 23" in games_in_wishlist
