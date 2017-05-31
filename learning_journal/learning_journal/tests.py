"""Test view functions."""
from pyramid import testing
from pyramid.response import Response
import pytest


@pytest.fixture
def list_response():
    """Return a response from the home page."""
    from learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    return response


@pytest.fixture
def detail_response():
    """Return a response from the home page."""
    from learning_journal.views.default import detail_view
    request = testing.DummyRequest()
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
    response = update_view(request)
    return response


def test_list_view_returns_response(list_response):
    """Test response a Response object."""
    assert isinstance(list_response, Response)


def test_list_view_good(list_response):
    """List view returns a Response object when given a request."""
    assert list_response.status_code == 200


def test_list_view_returns_content(list_response):
    """Test list_view returns correct content."""
    expected_text = u'<h1>Today I Learned ... <small>401 Python Learning Journal</small></h1>'
    print(dir(list_response))
    print(list_response)
    assert expected_text in list_response.text


def test_detail_view_returns_response(detail_response):
    """Test response a Response object."""
    assert isinstance(detail_response, Response)


def test_detail_view_good(detail_response):
    """Detail view returns a Response object when given a request."""
    assert detail_response.status_code == 200


def test_detail_view_returns_content(detail_response):
    """Detail list_view returns correct content."""
    expected_text = u'<h2>Another entry</h2>'
    assert expected_text in detail_response.text


def test_create_view_returns_response(create_response):
    """Test response a Response object."""
    assert isinstance(create_response, Response)


def test_create_view_good(create_response):
    """Create view returns a Response object when given a request."""
    assert create_response.status_code == 200


def test_create_view_returns_content(create_response):
    """Create list_view returns correct content."""
    expected_text = u'<div class="row" id="detail-entry">'
    assert expected_text in create_response.text


def test_update_view_returns_response(update_response):
    """Update response a Response object."""
    assert isinstance(update_response, Response)


def test_update_view_good(update_response):
    """Update view returns a Response object when given a request."""
    assert update_response.status_code == 200


def test_update_view_returns_content(update_response):
    """Update list_view returns correct content."""
    expected_text = u'<input type="button" class="btn btn-primary" value="Save Changes">'
    assert expected_text in update_response.text
