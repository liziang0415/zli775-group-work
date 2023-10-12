from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from games.domainmodel import Review
from games.services import find_game_by_title
from wtforms import TextAreaField, IntegerField, SubmitField

game_description_bp = Blueprint('game_description_bp', __name__)


@game_description_bp.route('/gameDescription', methods=['GET', 'POST'])
def game_description():
    from games.adapters.repository import repo_instance
    form = ReviewForm()
    game_title = request.args.get('title')
    game = find_game_by_title(repo_instance, game_title)
    if form.validate_on_submit():
        username = session['username']
        user = repo_instance.get_user(username)
        review = Review(user, game, form.rating.data, form.review_text.data)
        repo_instance.add_review(review)

        return redirect(url_for('game_description_bp.game_description', title=game_title))
    return render_template("gameDescription.html", game=game, form=form)


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (0-5)', [DataRequired(), NumberRange(min=0, max=5)])
    review_text = TextAreaField('Review', [DataRequired()])
    submit = SubmitField('Submit')
