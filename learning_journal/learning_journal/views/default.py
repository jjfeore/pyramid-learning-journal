"""Set up the default views."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from data.entries import ENTRIES


@view_config(route_name='list', renderer='../templates/list.jinja2')
def list_view(request):
    """Return index.html."""
    return {
        'page': 'Home',
        'entry': 'entries'
    }


@view_config(route_name='list', renderer='../templates/detail.jinja2')
def detail_view(request):
    """Return detail.html."""
    the_id = int(request.matchdict['id'])
    try:
        entry = ENTRIES[the_id]
    except IndexError:
        raise HTTPNotFound
    return {
        'page': 'Home',
        'entry': entry
    }


@view_config(route_name='list', renderer='../templates/new.jinja2')
def create_view(request):
    """Return new.html."""
    return {
        'page': 'New Entry'
    }


@view_config(route_name='list', renderer='../templates/edit.jinja2')
def update_view(request):
    """Return new.html."""
    the_id = int(request.matchdict['id'])
    try:
        entry = ENTRIES[the_id]
    except IndexError:
        raise HTTPNotFound
    return {
        'page': 'Edit Entry',
        'entry': entry
    }
