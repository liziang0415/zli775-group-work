import pytest
from games import create_app
from games.adapters.memory_repository import MemoryRepository


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    return repo
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost.localdomain'})
    return app

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='john_doe', password='SecurePass123',follow_redirects=False):
        return self.__client.post(
            '/login',
            data={'user_name': user_name, 'password': password},
        follow_redirects = follow_redirects
        )

    def logout(self):
        return self.__client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
