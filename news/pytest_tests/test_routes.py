import pytest
from http import HTTPStatus

from django.urls import reverse


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    '''Главная страница, страницы регистрации пользователей,
    входа в учётную запись и выхода из неё доступны анонимным пользователям.'''
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
