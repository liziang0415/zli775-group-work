from flask import Blueprint, render_template, request
from games.services import get_filtered_games
home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    from games.adapters.repository import repo_instance
    all_games = repo_instance.get_games()
    all_genres = set()
    all_publishers = set()

    for game in all_games:
        for genre in game.genres:
            all_genres.add(genre.genre_name)  # Use genre_name attribute
        all_publishers.add(game.publisher.publisher_name)  # Use publisher_name attribute

    return render_template('layout.html', all_genres=all_genres, all_publishers=all_publishers)


@home_bp.route('/search')
def search():
    from games.adapters.repository import repo_instance
    query = request.args.get('query', '')
    genre = request.args.get('genre', '')
    publisher = request.args.get('publisher', '')

    filtered_games = get_filtered_games(repo_instance, query, genre, publisher)

    if not filtered_games:
        return render_template('no_results.html'), 404

    return render_template('search_results.html', games=filtered_games, query=query, genre=genre, publisher=publisher)
