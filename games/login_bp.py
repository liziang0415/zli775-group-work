from functools import wraps
import bcrypt
from flask import Blueprint, render_template, url_for, flash, redirect, session
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from games.domainmodel.model import User

login_bp = Blueprint('login', __name__)


class NameNotUniqueException(Exception):
    pass


@login_bp.route("/register", methods=['GET', 'POST'])
def register():
    from games.adapters.repository import repo_instance
    form = RegistrationForm()
    username_not_unique = None

    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password)
            repo_instance.add_user(new_user)
            flash('Your account has been created!', 'success')
            return redirect(url_for('login.login'))
        except NameNotUniqueException:
            username_not_unique = 'Your username is already taken - please supply another'
    else:
        print(form.errors)

    return render_template('register.html', title='Register', form=form, username_error_message=username_not_unique)


@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    from games.adapters.repository import repo_instance
    form = LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None

    if form.validate_on_submit():
        user = repo_instance.get_user(form.username.data)
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            session['logged_in'] = True
            session['username'] = user.username
            flash('You have been logged in!', 'success')
            return redirect(url_for('home.home'))
        else:
            if not user:
                username_not_recognised = 'Username not recognised - please supply another'
            else:
                password_does_not_match_username = 'Password does not match supplied username - please check and try again'

    return render_template('login.html', title='Login', form=form, username_error_message=username_not_recognised,
                           password_error_message=password_does_not_match_username)


@login_bp.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('home.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('You need to be logged in to view this page.', 'danger')
            return redirect(url_for('login.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = 'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired(message='Your user name is required'),
                                        Length(min=2, max=20, message='Your user name is too short')])
    password = PasswordField('Password',
                             [DataRequired(message='Your password is required'), PasswordValid()])
    confirm_password = PasswordField('Confirm Password', [DataRequired(message='Your password is required'),
                                                          EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        from games.adapters.repository import repo_instance
        user = repo_instance.get_user(username.data)
        if user is not None:
            raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20, )])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
