import pytest


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Autor')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client
