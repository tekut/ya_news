import pytest

from news.models import News


@pytest.fixture
def news():
    news = News.objects.create(
        title='Title',
        text='Text',
    )
    return news
