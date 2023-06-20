import pytest
from django.conf import settings
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_news_count(client, all_news):
    '''Количество новостей на главной странице — не более 10'''
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, all_news):
    '''Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка'''
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, two_comments):
    '''Комментарии на странице отдельной новости отсортированы
    в хронологическом порядке: старые в начале списка, новые — в конце'''
    response = client.get(reverse('news:detail', args=(news.pk,)))
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


def test_anonymous_client_has_no_form(client, news):
    '''Анонимному пользователю недоступна форма для отправки
комментария на странице отдельной новости'''
    response = client.get(reverse('news:detail', args=(news.pk,)))
    assert 'form' not in response.context


def test_authorized_client_has_form(client, author, news):
    '''Авторизованному пользователю доступна форма для отправки
комментария'''
    client.force_login(author)
    response = client.get(reverse('news:detail', args=(news.pk,)))
    assert 'form' in response.context
