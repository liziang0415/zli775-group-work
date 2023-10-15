from urllib.parse import quote
from flask import session, url_for


def test_register(client):
    response_code = client.get("/register").status_code
    assert response_code == 200

    response = client.post(
        '/register',
        data={'username': 'peter_parker', 'password': 'Spiderman123', 'confirm_password': 'Spiderman123'}
    )
    assert response.status_code == 302


def test_register_with_invalid_input(client, app):  # Notice the addition of app fixture
    # Define a set of invalid inputs
    invalid_inputs = [
        {"username": "", "password": "SomePassword123", "confirm_password": "SomePassword123"},
        {"username": "short", "password": "shrt", "confirm_password": "shrt"},
        {"username": "user", "password": "password123", "confirm_password": "different123"},
        {"username": "test", "password": "test", "confirm_password": "test"},
    ]

    error_messages = [
        b'Your user name is required',
        b'Your password is required',
        b'Your user name is too short',
        b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit',
    ]

    with app.app_context():
        for invalid_input in invalid_inputs:
            response = client.post(url_for('login.register'), data=invalid_input)
            assert response.status_code == 200
            assert any(error_message in response.data for error_message in error_messages)



def test_login(client, auth):
    status_code = client.get('/login').status_code
    assert status_code == 200

    response = auth.login()
    assert response.status_code


def test_browse_games(client):
    response = client.get('/games')
    assert response.status_code == 200


def test_add_game_to_wishlist(client, auth):
    auth.login()

    game_title = "10 Second Ninja X"
    encoded_game_title = quote(game_title)
    response = client.get(f'/wishlist/add/{encoded_game_title}')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
