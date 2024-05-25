import pytest

from django.test.client import Client

from notes.models import Note

@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='not_author')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def note(author):
    note = Note.objects.create(
        title='test note',
        text='text for test note',
        slug='note_slug',
        author=author
    )
    return note


@pytest.fixture
def slug_for_args(note):
    return (note.slug,)
