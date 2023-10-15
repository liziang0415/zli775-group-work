from sqlalchemy import select, inspect
from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'games', 'genres', 'publishers',
                                           'reviews', 'users', 'wishlist_games', 'wishlists']


def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publishers_names = []
        for row in result:
            all_publishers_names.append(row['publisher_name'])

        assert len(all_publishers_names) == 798


def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append(row['genre_name'])

        assert len(all_genres) == 24


def test_database_populate_select_all_games(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['id'], row['title'], row['release_date'], row['description'],
                             row['image_url'], row['price'], row['publisher_name']))

        assert len(all_games) == 877


# def test_database_populate_select_all_reviews(database_engine):
#
#     # Get table information
#     inspector = inspect(database_engine)
#     name_of_reviews_table = inspector.get_table_names()[4]
#
#     with database_engine.connect() as connection:
#         # query for records in table comments
#         select_statement = select([metadata.tables[name_of_reviews_table]])
#         result = connection.execute(select_statement)
#
#         all_reviews = []
#         for row in result:
#             all_reviews.append((row['id'], row['game_id'], row['user_id'], row['rating'], row['comment']))
#
#         assert all_reviews == [(1, 435790, 1, 5, 'good'),
#                                (2, 1684530, 1, 5, 'nice')]
#
