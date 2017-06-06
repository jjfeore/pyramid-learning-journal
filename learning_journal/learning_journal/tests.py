"""Learning Journal tests."""
from pyramid import testing
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.models import JournalEntries, get_tm_session
from learning_journal.models.meta import Base
from faker import Faker
import datetime
import pytest
import transaction


FAKE_FACTORY = Faker()
JOURNAL_ENTRIES = [JournalEntries(
    title=FAKE_FACTORY.text(300),
    text=FAKE_FACTORY.text(300),
    author=FAKE_FACTORY.name(),
    date=datetime.datetime.now().strftime('%B %d, %Y')
) for i in range(20)]

random_entries = []


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database."""
    dummy_request.dbsession.add_all(JOURNAL_ENTRIES)


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://postgres:1234@localhost:5432/test_journal'
    })
    config.include("learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database."""
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def list_response():
    """Return a response from the list view."""
    from learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    return response


@pytest.fixture
def detail_response():
    """Return a response from the detail view."""
    from learning_journal.views.default import detail_view
    request = testing.DummyRequest()
    request.matchdict['id'] = 0
    response = detail_view(request)
    return response


@pytest.fixture
def create_response():
    """Return a response from the create view."""
    from learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    return response


@pytest.fixture
def update_response():
    """Return a response from the update view."""
    from learning_journal.views.default import update_view
    request = testing.DummyRequest()
    request.matchdict['id'] = 0
    response = update_view(request)
    return response


@pytest.fixture(scope="session")
def testapp(request):
    """Create a test application for functional tests."""
    from webtest import TestApp

    def main(global_config, **settings):
        """Return a Pyramid WSGI application."""
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({}, **{
        'sqlalchemy.url': 'postgres://postgres:1234@localhost:5432/test_journal'
    })
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """File the DB."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        for i in range(20):
            the_title = FAKE_FACTORY.text(300)
            the_text = FAKE_FACTORY.text(300)
            the_author = FAKE_FACTORY.name()
            the_date = datetime.datetime.now().strftime('%B %d, %Y')
            random_entries.append([the_title, the_text, the_author, the_date])
            row = JournalEntries(
                title=the_title,
                text=the_text,
                author=the_author,
                date=the_date
            )
            dbsession.add(row)


def test_detail_view_with_id_raises_except(dummy_request):
    """Calling the detail view route with an invalid id returns an error."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = '1000'
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_update_view_with_id_raises_except(dummy_request):
    """Calling the update view route with an invalid id returns an error."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = '1000'
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_entries():
    """Test if the rand-generated entries are valid Journal Entries."""
    assert isinstance(JOURNAL_ENTRIES[0], JournalEntries)


def test_model_gets_added(db_session):
    """Test to see if we can instantiate and load a DB."""
    assert len(db_session.query(JournalEntries).all()) == 0
    model = JournalEntries(
        title=u"Fake Category",
        date=datetime.datetime.now().strftime('%B %d, %Y'),
        author=u"Whoever",
        text=u"Some text in the body"
    )
    db_session.add(model)
    assert len(db_session.query(JournalEntries).all()) == 1


def test_list_view_returns_dict(dummy_request):
    """List view returns a dictionary of values."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response, dict)


def test_list_view_returns_empty_when_database_empty(dummy_request):
    """List view returns nothing when there is no data."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert len(response['entry']) == 0


def test_list_view_returns_count_matching_database(dummy_request, add_models):
    """List view response matches database count."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    query = dummy_request.dbsession.query(JournalEntries)
    assert len(response['entry']) == query.count()


def test_create_view_post_empty_is_empty_dict(dummy_request):
    """POST requests should return empty dictionary."""
    from learning_journal.views.default import create_view
    dummy_request.method = 'POST'
    response = create_view(dummy_request)
    assert response == {}


def test_create_view_post_incomplete_data_returns_data(dummy_request):
        """Incomplete POST data returned to user."""
        from learning_journal.views.default import create_view
        dummy_request.method = "POST"
        post_data = {
            'title': '',
            'text': FAKE_FACTORY.text(300),
            'error': "Please fill all form elements."
        }
        dummy_request.POST = post_data
        response = create_view(dummy_request)
        assert response == post_data


def test_create_view_post_with_data_302(dummy_request):
        """POST request with correct data should redirect with status code 302."""
        from learning_journal.views.default import create_view
        dummy_request.method = "POST"
        post_data = {
            'title': FAKE_FACTORY.text(50),
            'text': FAKE_FACTORY.text(300)
        }
        dummy_request.POST = post_data
        import pdb; pdb.set_trace()
        response = create_view(dummy_request)
        assert response.status_code == 302


# def test_list_route_returns_list_content(testapp, fill_the_db):
#     """Test list route creates page that has list entries."""
#     response = testapp.get('/')
#     html = response.html
#     post_count = html.find_all('h2')
#     assert html.find('h2').text in random_entries[-1][0]
#     assert len(post_count) == len(JOURNAL_ENTRIES)


# def test_list_view_returns_dict(dummy_request):
#     """List view returns a dictionary of values."""
#     from learning_journal.views.default import list_view
#     response = list_view(dummy_request)
#     assert isinstance(response, dict)


# def test_list_view_returns_empty_when_database_empty(dummy_request):
#     """List view returns nothing when there is no data."""
#     from learning_journal.views.default import list_view
#     response = list_view(dummy_request)
#     assert len(response['entry']) == 0


# def test_list_view_returns_count_matching_database(dummy_request, add_models):
#     """List view response matches database count."""
#     from learning_journal.views.default import list_view
#     response = list_view(dummy_request)
#     query = dummy_request.dbsession.query(JournalEntries)
#     assert len(response['entry']) == query.count()
