from flask import Blueprint, render_template, request
from .adapters.datareader import GameFileCSVReader

games_bp = Blueprint('games_bp', __name__)


@games_bp.route('/games')
def game():
    page = request.args.get('page', 1, type=int)
    genre_filter = request.args.get('genre', None)
    per_page = 18
    offset = (page - 1) * per_page
    sort_order = request.args.get('sort', 'title')

    reader = GameFileCSVReader("games/adapters/datareader/games.csv")
    reader.read_csv_file()
    game_list = reader.dataset_of_games
    all_genres = reader.dataset_of_genres

    if genre_filter:
        game_list = [game for game in game_list if genre_filter in [genre.genre_name for genre in game.genres]]

    if sort_order == 'release_date':
        game_list.sort(key=lambda x: x.release_date)
    elif sort_order == 'price':
        game_list.sort(key=lambda x: x.price, reverse=True)  # Assuming price is a numeric value
    else:  # Default to sorting by title
        game_list.sort(key=lambda x: x.title.lower())  # Sorting alphabetically, case-insensitive

    games_to_display = game_list[offset:offset + per_page]

    return render_template("games.html", games=games_to_display, page=page, current_genre=genre_filter,
                           genres=all_genres, current_sort=sort_order)

@games_bp.route('/gameDescription')
def game_description():
    game_title = request.args.get('title')
    if game_title:
        reader = GameFileCSVReader("games/adapters/datareader/games.csv")
        reader.read_csv_file()
        game_list = reader.dataset_of_games

        for game in game_list:
            if game.title == game_title:
                return render_template("gameDescription.html", game=game)