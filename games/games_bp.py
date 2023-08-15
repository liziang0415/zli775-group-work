from flask import Blueprint, render_template, request
from .adapters.datareader import GameFileCSVReader

games_bp = Blueprint('games_bp', __name__)


@games_bp.route('/games')
def game():
    page = request.args.get('page', 1, type=int)
    genre_filter = request.args.get('genre', None)
    per_page = 18
    offset = (page - 1) * per_page

    reader = GameFileCSVReader("games/adapters/datareader/games.csv")
    reader.read_csv_file()
    nmsl = reader.dataset_of_games

    all_genres = reader.dataset_of_genres  # Retrieve all unique genres

    if genre_filter:
        nmsl = [game for game in nmsl if genre_filter in [genre.genre_name for genre in game.genres]]

    nmsl.sort(key=lambda x: x.title)
    games_to_display = nmsl[offset:offset + per_page]

    return render_template("games.html", games=games_to_display, page=page, current_genre=genre_filter,
                           genres=all_genres)
