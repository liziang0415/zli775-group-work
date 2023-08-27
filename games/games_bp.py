from flask import Blueprint, render_template, request
from games.services import get_filtered_and_sorted_games
games_bp = Blueprint('games_bp', __name__)


@games_bp.route('/games')
def game():
    from games.adapters.repository import repo_instance

    page = request.args.get('page', 1, type=int)
    genre_filter = request.args.get('genre', None)
    sort_order = request.args.get('sort', 'title')

    games_to_display, all_genres = get_filtered_and_sorted_games(repo_instance, page, genre_filter, sort_order)
    return render_template("games.html", games=games_to_display, page=page, current_genre=genre_filter,
                           genres=all_genres, current_sort=sort_order)

