from flask import Blueprint, render_template, flash, redirect, session, request
from games.login_bp import login_required

wishlist_bp = Blueprint('wishlist', __name__)


@wishlist_bp.route("/add/<string:game_title>", methods=['GET'])
@login_required
def add(game_title):
    from games.adapters.repository import repo_instance
    username = session['username']
    game = repo_instance.get_game_by_title(game_title)
    if game:
        if repo_instance.is_in_wishlist(username, game):
            flash(f'{game.title} is already in your wishlist!', 'info')
        else:
            repo_instance.add_to_wishlist(username, game)
            flash(f'{game.title} has been added to your wishlist!', 'success')
    else:
        flash(f'{game_title} does not exist!', 'danger')
    return redirect(request.referrer)


@wishlist_bp.route("/remove/<string:game_title>", methods=['GET'])
@login_required
def remove(game_title):
    from games.adapters.repository import repo_instance
    username = session['username']
    game = repo_instance.get_game_by_title(game_title)
    if game:
        if not repo_instance.is_in_wishlist(username, game):
            flash(f'{game.title} is not in your wishlist!', 'info')
        else:
            repo_instance.remove_from_wishlist(username, game)
            flash(f'{game.title} has been removed from your wishlist!', 'success')
    else:
        flash(f'{game_title} does not exist!', 'danger')
    return redirect(request.referrer)


@wishlist_bp.route("/", methods=['GET'])
@login_required
def view_wishlist():
    from games.adapters.repository import repo_instance
    username = session['username']
    wishlist = repo_instance.get_wishlist(username)
    if wishlist is None:
        wishlist = []
    return render_template('wishlist.html', wishlist=wishlist)
