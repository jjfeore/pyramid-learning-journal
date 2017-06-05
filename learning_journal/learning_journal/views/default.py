"""Set up the default views."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from learning_journal.models import JournalEntries
import datetime


@view_config(route_name='list', renderer='../templates/list.jinja2')
def list_view(request):
    """Return the list view."""
    session = request.dbsession
    entry = session.query(JournalEntries).order_by(JournalEntries.id.desc()).all()
    return {
        'page': 'Home',
        'entry': entry
    }


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """Return  the detail view."""
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    entry = session.query(JournalEntries).get(the_id)
    if not entry:
        raise HTTPNotFound
    return {
        'page': entry.title,
        'title': entry.title,
        'author': entry.author,
        'date': entry.date,
        'id': entry.id,
        'text': entry.text
    }


@view_config(route_name='create', renderer='../templates/new.jinja2')
def create_view(request):
    """Return the create view."""
    if request.method == "POST" and request.POST:
        if not request.POST['title'] or not request.POST['text']:
            return {
                'title': request.POST['title'],
                'text': request.POST['text'],
                'error': "Please fill all form elements."
            }
        new_entry = JournalEntries(
            title=request.POST['title'],
            author=u'James Feore',
            text=request.POST['text'],
            date=datetime.datetime.now().strftime('%B %d, %Y')
        )
        request.dbsession.add(new_entry)
        return HTTPFound(
            location=request.route_url('list')
        )

    return {}


@view_config(route_name='update', renderer='../templates/edit.jinja2')
def update_view(request):
    """Return the update view."""
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    entry = session.query(JournalEntries).get(the_id)
    if not entry:
        raise HTTPNotFound
    if request.method == "GET":
        return {
            'page': 'Edit Entry',
            'title': entry.title,
            'text': entry.text
        }
    if request.method == "POST":
        entry.title = request.POST['title']
        entry.text = request.POST['text']
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail', id=entry.id))
