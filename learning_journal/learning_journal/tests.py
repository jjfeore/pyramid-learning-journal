"""Test view functions."""


from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.views.data.entries import ENTRIES
import pytest


@pytest.fixture
def list_response():
    """Return a response from the list view."""
    from learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    return response


@pytest.fixture
def detail_response():
    """Return a response from the home page."""
    from learning_journal.views.default import detail_view
    request = testing.DummyRequest()
    request.matchdict['id'] = 0
    response = detail_view(request)
    return response


@pytest.fixture
def create_response():
    """Return a response from the home page."""
    from learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    return response


@pytest.fixture
def update_response():
    """Return a response from the home page."""
    from learning_journal.views.default import update_view
    request = testing.DummyRequest()
    request.matchdict['id'] = 0
    response = update_view(request)
    return response


def test_list_view_returns_proper_content(list_response):
    """List view response includes the content we added."""
    # import pdb; pdb.set_trace()
    assert 'page' in list_response
    assert 'entry' in list_response
    assert list_response['entry'] == ENTRIES


def test_detail_view_returns_proper_content(detail_response):
    """Detail view response includes the content we added."""
    assert detail_response['page'] == detail_response['entry']['title']
    assert 'entry' in detail_response
    assert detail_response['entry'] in ENTRIES


def test_create_view_returns_proper_content(create_response):
    """Create view response includes the content we added."""
    assert 'page' in create_response


def test_update_view_returns_proper_content(update_response):
    """Update view response includes the content we added."""
    assert 'page' in update_response
    assert 'entry' in update_response
    assert update_response['entry'] in ENTRIES


def test_detail_view_with_id_returns_one_entry():
    """."""
    from learning_journal.views.default import detail_view
    req = testing.DummyRequest()
    req.matchdict['id'] = '1'
    response = detail_view(req)
    assert response['entry'] == ENTRIES[1]


def test_detail_view_with_bad_id_raises_exception():
    """."""
    from learning_journal.views.default import detail_view
    req = testing.DummyRequest()
    req.matchdict['id'] = '1337'
    with pytest.raises(HTTPNotFound):
        detail_view(req)


@pytest.fixture
def testapp():
    """Create a test application to use for functional tests."""
    from learning_journal import main
    from webtest import TestApp
    app = main({})
    return TestApp(app)


def test_list_route_returns_home_content(testapp):
    """."""
    response = testapp.get('/')
    html = response.html
    assert 'Today I Learned ...' in str(html.find('h1').text)
    assert 'James Feore\'s Learning Journal - Home' in str(html.find('title').text)


def test_routes_with_bad_ids(testapp):
    """Test detail and edit routes with bad ids."""
    assert "Learning Journal Page Failure" in testapp.get('/journal/789', status=404).text
    assert "Learning Journal Page Failure" in testapp.get('/journal/789/edit-entry', status=404).text
