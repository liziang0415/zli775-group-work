from games.adapters.repository import AbstractRepository


def get_all_games(repo: AbstractRepository):
    return repo.get_games()


def get_filtered_games(repo: AbstractRepository, query='', genre='', publisher=''):
    all_games = repo.get_games()
    return [
        game for game in all_games if
        (query.lower() in game.title.lower() or query.lower() in game.publisher.publisher_name.lower()) and
        (not genre or any(g.genre_name == genre for g in game.genres)) and
        (not publisher or publisher == game.publisher.publisher_name)
    ]


def find_game_by_title(repo: AbstractRepository, title: str):
    all_games = repo.get_games()
    for game in all_games:
        if game.title == title:
            return game
    return None


def get_filtered_and_sorted_games(repo: AbstractRepository, page=1, genre_filter=None, sort_order='title'):
    all_games = repo.get_games()

    all_genres = set()
    for game in all_games:
        for genre in game.genres:
            all_genres.add(genre.genre_name)

    if genre_filter:
        all_games = [game for game in all_games if genre_filter in [genre.genre_name for genre in game.genres]]

    if sort_order == 'release_date':
        all_games.sort(key=lambda x: x.release_date)
    elif sort_order == 'price':
        all_games.sort(key=lambda x: x.price, reverse=True)
    else:
        all_games.sort(key=lambda x: x.title.lower())

    per_page = 18
    offset = (page - 1) * per_page
    games_to_display = all_games[offset:offset + per_page]

    return games_to_display, all_genres
