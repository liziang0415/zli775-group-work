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