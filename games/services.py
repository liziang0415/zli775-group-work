from datetime import datetime


def get_all_games(repo):
    return repo.get_games()


def get_sorted_publisher_and_genres(repo):
    all_publisher = set()
    all_genres = set()
    all_games = repo.get_games()
    for game in all_games:
        for genre in game.genres:
            all_genres.add(genre.genre_name)
        all_publisher.add(game.publisher.publisher_name)
    all_genres = list(all_genres)
    all_genres = sorted(all_genres)
    all_publisher = list(all_publisher)
    all_publisher = sorted(all_publisher)
    return all_publisher, all_genres


def get_filtered_games(repo, query='', genre='', publisher=''):
    all_games = repo.get_games()
    return [
        game for game in all_games if
        (query.lower() in game.title.lower() or query.lower() in game.publisher.publisher_name.lower()) and
        (not genre or any(g.genre_name == genre for g in game.genres)) and
        (not publisher or publisher == game.publisher.publisher_name)
    ]


def find_game_by_title(repo, title: str):
    all_games = repo.get_games()
    for game in all_games:
        if game.title == title:
            return game
    return None


def get_filtered_and_sorted_games(repo, page=1, genre_filter=None, sort_order='title'):
    all_games = repo.get_games()

    all_genres = set()
    for game in all_games:
        for genre in game.genres:
            all_genres.add(genre.genre_name)

    if genre_filter:
        all_games = [game for game in all_games if genre_filter in [genre.genre_name for genre in game.genres]]

    if sort_order == 'release_date':
        all_games.sort(key=lambda x: datetime.strptime(x.release_date, "%b %d, %Y") if x.release_date else datetime.min,
                       reverse=True)
        all_games.sort(key=lambda x: datetime.strptime(x.release_date, "%b %d, %Y") if x.release_date else datetime.min,
                       reverse=True)
    elif sort_order == 'price':
        all_games.sort(key=lambda x: x.price, reverse=True)
    else:
        all_games.sort(key=lambda x: x.title.lower())

    per_page = 18
    offset = (page - 1) * per_page
    games_to_display = all_games[offset:offset + per_page]
    total_pages = (len(all_games) + per_page - 1) // per_page

    return games_to_display, total_pages


class NameNotUniqueException(Exception):
    pass
