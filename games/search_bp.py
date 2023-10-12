from flask import Blueprint, render_template, request
from games.services import get_filtered_games, get_sorted_publisher_and_genres

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search():
    from games.adapters.repository import repo_instance
    query = request.args.get('query', '')
    genre = request.args.get('genre', '')
    publisher = request.args.get('publisher', '')

    filtered_games = get_filtered_games(repo_instance, query, genre, publisher)
    all_publisher, all_genres = get_sorted_publisher_and_genres(repo_instance)

    if not filtered_games:
        return render_template('no_results.html'), 404

    return render_template('search_results.html', games=filtered_games, query=query, genre=genre, publisher=publisher,
                           all_genres=all_genres,
                           all_publishers=all_publisher)
