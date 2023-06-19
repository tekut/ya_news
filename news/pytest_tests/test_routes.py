import pytest
from http import HTTPStatus

from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    '''Главная страница, страницы отдельной новости, регистрации пользователей,
    входа в учётную запись и выхода из неё доступны анонимным пользователям.'''
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_details_availability_for_anonymous_user(client, news):
    '''Страница отдельной новости доступна анонимному пользователю'''
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
