import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    '''Главная страница, страницы регистрации пользователей,
    входа в учётную запись и выхода из неё доступны анонимным пользователям'''
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_details_availability_for_anonymous_user(client, news):
    '''Страница отдельной новости доступна анонимному пользователю'''
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, comment, expected_status
):
    '''Страницы удаления и редактирования комментария доступны
    автору комментария.
    Авторизованный пользователь не может зайти на страницы
      редактирования или удаления чужих комментариев
      (возвращается ошибка 404)'''
    url = reverse(name, args=(comment.pk,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('comment_pk')),
        ('news:delete', pytest.lazy_fixture('comment_pk')),
    ),
)
def test_redirects(client, name, args):
    '''При попытке перейти на страницу редактирования или
    удаления комментария анонимный пользователь перенаправляется
    на страницу авторизации'''
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
