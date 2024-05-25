import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects

from django.urls import reverse


@pytest.mark.parametrize(
        'name',
        ('notes:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_for_anon_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
        'name',
        ('notes:list', 'notes:add', 'notes:success',)
)
def test_pages_for_auth_user(not_author_client, name):
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
        'param_client, expected_status',
        (
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
            (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        )
)
@pytest.mark.parametrize(
        'name',
        ('notes:detail', 'notes:edit', 'notes:delete')
)
def test_note_pages_avaliability(
    param_client,
    name,
    note,
    expected_status
):
    url = reverse(name, args=(note.slug,))
    response = param_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
        'name, note_args',
        (
            ('notes:detail', pytest.lazy_fixture('slug_for_args')),
            ('notes:edit', pytest.lazy_fixture('slug_for_args')),
            ('notes:delete', pytest.lazy_fixture('slug_for_args')),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None),
        )
)
def test_redirect_to_login(
        client,
        name,
        note_args
):
    login_url = reverse('users:login')
    url = reverse(name, args=note_args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
