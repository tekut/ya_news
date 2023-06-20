from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Title',
        text='Text',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',

    )
    return comment


@pytest.fixture
def comment_pk(comment):
    return comment.pk,


@pytest.fixture
def all_news():
    all_news = News.objects.bulk_create(
        News(
            title=f'Title {i}',
            text='Text',
            date=datetime.today().date() - timedelta(days=i),
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return all_news


@pytest.fixture
def two_comments(author, news):
    for i in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Comment {i}',
        )
        comment.created = timezone.now() + timedelta(days=i)
        comment.save()
    return two_comments


@pytest.fixture
def form_data():
    return {
        'text': 'Обновлённый комментарий',
    }
