import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, news, form_data):
    '''Анонимный пользователь не может отправить комментарий'''
    client.post(reverse('news:detail', args=(news.pk,)), data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, author, news, form_data):
    '''Авторизованный пользователь может отправить комментарий'''
    URL = reverse('news:detail', args=(news.pk,))
    response = author_client.post(URL, data=form_data)
    assertRedirects(response, f'{URL}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(news, author_client):
    '''Если комментарий содержит запрещённые слова,
    он не будет опубликован, а форма вернёт ошибку'''
    URL = reverse('news:detail', args=(news.pk,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(URL, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
        )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, news, comment):
    '''Авторизованный пользователь может удалять свои комментарии'''
    news_url = reverse('news:detail', args=(news.pk,))
    url_to_comments = news_url + '#comments'
    url_delete = reverse('news:delete', args=(comment.pk,))
    response = author_client.delete(url_delete)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(admin_client, comment):
    '''Авторизованный пользователь не может удалять чужие комментарии'''
    url_delete = reverse('news:delete', args=(comment.pk,))
    response = admin_client.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(author_client, news, comment, form_data):
    '''Авторизованный пользователь может редактировать свои комментарии'''
    NEW_COMMENT_TEXT = 'Обновлённый комментарий'
    news_url = reverse('news:detail', args=(news.pk,))
    url_edit = reverse('news:edit', args=(comment.pk,))
    url_to_comments = news_url + '#comments'
    response = author_client.post(url_edit, data=form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(admin_client,
                                                comment,
                                                form_data,
                                                ):
    '''Авторизованный пользователь не может редактировать чужие комментарии'''
    COMMENT_TEXT = 'Текст комментария'
    url_edit = reverse('news:edit', args=(comment.pk,))
    response = admin_client.post(url_edit, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
