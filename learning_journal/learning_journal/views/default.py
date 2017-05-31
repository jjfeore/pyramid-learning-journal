"""Set up the default views."""
from pyramid.response import Response
from os import path


HERE = path.dirname(__file__)


def list_view(request):
    """Return index.html."""
    with open(path.join(HERE, '../templates/index.html')) as web_page:
        ret_page = web_page.read()
    return Response(ret_page)


def detail_view(request):
    """Return detail.html."""
    with open(path.join(HERE, '../templates/detail.html')) as web_page:
        ret_page = web_page.read()
    return Response(ret_page)


def create_view(request):
    """Return new.html."""
    with open(path.join(HERE, '../templates/new.html')) as web_page:
        ret_page = web_page.read()
    return Response(ret_page)


def update_view(request):
    """Return edit.html."""
    with open(path.join(HERE, '../templates/edit.html')) as web_page:
        ret_page = web_page.read()
    return Response(ret_page)
