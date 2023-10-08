from flask import Blueprint, render_template, session
from .login_bp import login_required
user_profile_bp = Blueprint('user_profile', __name__)


@user_profile_bp.route('/user_profile', methods=['GET'])
@login_required
def user_profile():
    from games.adapters.repository import repo_instance
    username = session['username']
    user = repo_instance.get_user(username)
    reviews = user.reviews
    wishlist = user.favourite_games

    return render_template('user_profile.html', user=user, reviews=reviews, wishlist=wishlist)