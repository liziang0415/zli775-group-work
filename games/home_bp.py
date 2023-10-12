from flask import Blueprint, render_template
from .services import get_sorted_publisher_and_genres
home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    from games.adapters.repository import repo_instance
    all_publishers, all_genres = get_sorted_publisher_and_genres(repo_instance)

    return render_template('home.html', all_genres=all_genres, all_publishers=all_publishers)

