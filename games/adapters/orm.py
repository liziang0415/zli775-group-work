from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, ForeignKey, Float, Date, Text, JSON
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist

metadata = MetaData()

publishers = Table(
    'publishers', metadata,
    Column('publisher_name', String(255), primary_key=True)
)

genres = Table(
    'genres', metadata,
    Column('genre_name', String(255), primary_key=True)
)

games = Table(
    'games', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('release_date', String(255), nullable=True),
    Column('description', Text, nullable=True),
    Column('image_url', String(255), nullable=True),
    Column('price', Float, nullable=True),
    Column('publisher_name', String(255), ForeignKey('publishers.publisher_name')),
)

game_genres = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('genre_name', String(255), ForeignKey('genres.genre_name'))
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), nullable=False, unique=True),
    Column('password', String(255), nullable=False),
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('rating', Integer, nullable=False),
    Column('comment', Text, nullable=True)
)

wishlists = Table(
    'wishlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
)

wishlist_games = Table(
    'wishlist_games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('wishlist_id', Integer, ForeignKey('wishlists.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
)



def map_model_to_tables():
    # Publisher mapping
    mapper(Publisher, publishers, properties={
        '_Publisher__publisher_name': publishers.c.publisher_name
    })

    # Genre mapping
    mapper(Genre, genres, properties={
        '_Genre__genre_name': genres.c.genre_name,
    })

    # Game mapping
    mapper(Game, games, properties={
        '_Game__game_id': games.c.id,
        '_Game__game_title': games.c.title,
        '_Game__release_date': games.c.release_date,
        '_Game__description': games.c.description,
        '_Game__image_url': games.c.image_url,
        '_Game__price': games.c.price,
        '_Game__publisher': relationship(Publisher, backref='games', foreign_keys=[games.c.publisher_name]),
        '_Game__genres': relationship(Genre, secondary=game_genres),
        '_Game__reviews': relationship(Review, back_populates='_Review__game'),
    })

    # User mapping
    mapper(User, users, properties={
        '_User__username': users.c.username,
        '_User__password': users.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        '_User__wishlist': relationship(Wishlist, uselist=False, back_populates='_Wishlist__user')
    })

    # Review mapping
    mapper(Review, reviews, properties={
        '_Review__rating': reviews.c.rating,
        '_Review__comment': reviews.c.comment,
        '_Review__user_id': reviews.c.user_id,
        '_Review__game_id': reviews.c.game_id,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__game': relationship(Game, back_populates='_Game__reviews')
    })

    # Wishlist mapping
    mapper(Wishlist, wishlists, properties={
        '_Wishlist__user': relationship(User, back_populates='_User__wishlist'),
        '_Wishlist__list_of_games': relationship(Game, secondary=wishlist_games)
    })

