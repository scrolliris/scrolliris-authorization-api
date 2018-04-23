import json

import pytest
import pyramid.httpexceptions as exc
from pyramid.response import Response
from webob.multidict import NestedMultiDict

from bern.view import issue_token

from ..conftest import dummy_find_service


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):
    # pylint: disable=unused-argument
    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_issue_token_response_no_api_key(monkeypatch, dummy_request):
    monkeypatch.setattr(dummy_request, 'find_service',
                        dummy_find_service('789'))

    dummy_request.env = {
        'RESPONSE_PREFIX': ''
    }
    dummy_request.accept = 'application/json'
    dummy_request.matchdict = {
        'project_id': '123',
    }

    with pytest.raises(exc.HTTPForbidden):
        issue_token(dummy_request)


def test_issue_token_response_accept_mismatch(monkeypatch, dummy_request):
    monkeypatch.setattr(dummy_request, 'find_service',
                        dummy_find_service('789'))

    dummy_request.env = {
        'RESPONSE_PREFIX': ''
    }
    dummy_request.accept = 'text/html'
    dummy_request.matchdict = {
        'project_id': '123',
    }
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'api_key': '456',
    })

    with pytest.raises(exc.HTTPNotFound):
        issue_token(dummy_request)


def test_issue_token_response_prefix(monkeypatch, dummy_request):
    monkeypatch.setattr(dummy_request, 'find_service',
                        dummy_find_service('789'))

    dummy_request.env = {
        'RESPONSE_PREFIX': '12345'
    }
    dummy_request.accept = 'application/json'
    dummy_request.matchdict = {
        'project_id': '123',
    }
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'api_key': '456',
    })

    res = issue_token(dummy_request)
    assert isinstance(res, Response)

    body = res.body.decode()
    assert body.startswith('12345')


def test_issue_token_is_not_generated(monkeypatch, dummy_request):
    monkeypatch.setattr(dummy_request, 'find_service',
                        dummy_find_service(None))

    dummy_request.env = {
        'RESPONSE_PREFIX': ''
    }
    dummy_request.accept = 'application/json'
    dummy_request.matchdict = {
        'project_id': '123',
    }
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'api_key': '456',
    })

    with pytest.raises(exc.HTTPInternalServerError):
        issue_token(dummy_request)


def test_issue_token_response(monkeypatch, dummy_request):
    monkeypatch.setattr(dummy_request, 'find_service',
                        dummy_find_service('789'))

    dummy_request.env = {
        'RESPONSE_PREFIX': ''
    }
    dummy_request.accept = 'application/json'
    dummy_request.matchdict = {
        'project_id': '123',
    }
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'api_key': '456',
    })

    res = issue_token(dummy_request)
    assert isinstance(res, Response)

    data = json.loads(res.body.decode())
    assert isinstance(data, dict)
    assert '789' == data.get('token')
