from flask import Blueprint, render_template, request
from games.services import find_game_by_title

game_description_bp = Blueprint('game_description_bp', __name__)


@game_description_bp.route('/gameDescription')
def game_description():
    from games.adapters.repository import repo_instance
    game_title = request.args.get('title')
    if game_title:
        game = find_game_by_title(repo_instance, game_title)
        if game:
            genre_names = [genre.genre_name for genre in game.genres]
            genre_str = ', '.join(genre_names)
            return render_template("gameDescription.html", game=game, genre_str=genre_str)
        else:
            return render_template('no_results.html'), 404
