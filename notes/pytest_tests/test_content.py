import pytest

from django.urls import reverse

from notes.forms import NoteForm


@pytest.mark.parametrize(
     'param_client, note_in_list',
     (
         (pytest.lazy_fixture('author_client'), True),
         (pytest.lazy_fixture('not_author_client'), False),
     )
)
def test_note_in_list_for_author(note, param_client, note_in_list):
    url = reverse('notes:list')
    response = param_client.get(url)
    object_list = response.context['object_list']
    assert (note in object_list) is note_in_list


@pytest.mark.parametrize(
        'name, args',
        (
            ('notes:add', None),
            ('notes:edit', pytest.lazy_fixture('slug_for_args'))
        )
)
def test_note_pages_contains_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], NoteForm)
