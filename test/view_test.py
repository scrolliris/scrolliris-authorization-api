import json

import pytest
import pyramid.httpexceptions as exc
from pyramid.response import Response
from webob.multidict import NestedMultiDict

from bern.view import issue_token


@pytest.fixture(autouse=True)
def setup(request, mocker, config):
    # pylint: disable=unused-argument
    mocker.patch('pyramid_services.find_service', autospec=True)

    def teardown():
        mocker.stopall()

    request.addfinalizer(teardown)


def test_issue_token_response_no_api_key(dummy_request):
    dummy_request.env = {
        'RESPONSE_PREFIX': ''
    }
    dummy_request.accept = 'application/json'
    dummy_request.matchdict = {
        'project_id': '123',
    }

    with pytest.raises(exc.HTTPForbidden):
        issue_token(dummy_request)


def test_issue_token_response_accept_mismatch(dummy_request):
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


def test_issue_token_response(dummy_request):
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
    assert {} == json.loads(res.body.decode())
