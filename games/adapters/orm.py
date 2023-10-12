<<<<<<< Updated upstream
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float, Date, DateTime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper, relationship, registry

from games.domainmodel import model

DATABASE_URL = "sqlite:///games.db"

engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, unique=True, nullable=True)
)
genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, unique=True, nullable=False)
)

games_table = Table(
    'games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, unique=True, nullable=False),
    Column('price', Float),
    Column('release_date', Date),
    Column('description', String),
    Column('image_url', String),
    Column('website_url', String),
    Column('publisher_id', ForeignKey('publishers.id'))
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('game_id', ForeignKey('games.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String, unique=True, nullable=False),
    Column('password', String, nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('game_id', ForeignKey('games.id')),
    Column('rating', Integer),
    Column('comment', String),
    Column('timestamp', DateTime, default=datetime.now)
)

wishlists_table = Table(
    'wishlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('game_id', ForeignKey('games.id'))
)


mapper_registry = registry()

def map_model_to_tables():
    try:
        mapper_registry.map_imperatively(model.Publisher, publishers_table)

        mapper_registry.map_imperatively(model.Genre, genres_table, properties={
            'games': relationship(model.Game, secondary=game_genres_table, back_populates='genres')
        })

        mapper_registry.map_imperatively(model.Game, games_table, properties={
            'publisher': relationship(model.Publisher),
            'genres': relationship(model.Genre, secondary=game_genres_table, back_populates='games'),
            'reviews': relationship(model.Review, backref='game'),
            'users_wishing': relationship(model.User, secondary=wishlists_table, back_populates='wishlist')
        })

        mapper_registry.map_imperatively(model.User, users_table, properties={
            'reviews': relationship(model.Review, backref='user'),
            'wishlist': relationship(model.Game, secondary=wishlists_table, back_populates='users_wishing')
        })

        mapper_registry.map_imperatively(model.Review, reviews_table)

    except Exception as e:
        print(f"Error mapping models to tables: {e}")
=======
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, ForeignKey, Float, Date, Text
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
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('rating', Integer, nullable=False),
    Column('comment', Text, nullable=True)
)

wishlists = Table(
    'wishlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'))
)

wishlist_games = Table(
    'wishlist_games', metadata,
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
        '_Game__reviews': relationship(Review, backref='game'),
        'wishlists': relationship(Wishlist, secondary=wishlist_games, back_populates="games")
    })

    # User mapping
    mapper(User, users, properties={
        '_User__username': users.c.username,
        '_User__password': users.c.password,
        'reviews': relationship(Review, backref='user'),
        'wishlist': relationship(Wishlist, uselist=False, backref='user')
    })

    # Review mapping
    mapper(Review, reviews, properties={
        '_Review__rating': reviews.c.rating,
        '_Review__comment': reviews.c.comment,
        'user_id': reviews.c.user_id,
        'game_id': reviews.c.game_id
    })

    # Wishlist mapping
    mapper(Wishlist, wishlists, properties={
        'user_id': wishlists.c.user_id,
        'games': relationship(Game, secondary=wishlist_games, back_populates="wishlists")
    })
>>>>>>> Stashed changes
