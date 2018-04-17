import collections

import pytest


def routing_to(version_id='v1.0', project_id='123', path='token'):
    return '/{:s}/projects/{:s}/credentials/{:s}'.format(
        version_id, project_id, path)


@pytest.fixture(autouse=True)
def setup(request, mocker, config):
    # pylint: disable=unused-argument
    mocker.patch('pyramid_services.find_service', autospec=True)

    def teardown():
        mocker.stopall()

    request.addfinalizer(teardown)


def test_route_path_to_token(dummy_request):
    route_path = dummy_request.route_path(
        'issue_token',
        project_id='123',
        _query=collections.OrderedDict([
            ('api_key', '456'),
            ('action', 'read'),
        ]))

    assert '/v1.0/projects/123/credentials/' \
           'token?api_key=456&action=read' == route_path


def test_routing_to_token_read(dummy_app):
    url = routing_to(version_id='v1.0', project_id='123', path='token')
    params = {
        'api_key': '456',
        'action': 'read',
    }
    headers = {
        'Accept': 'application/json'
    }
    res = dummy_app.get(url, params, headers, status=200)
    assert 200 == res.status_code


def test_routing_to_token_write(dummy_app):
    url = routing_to(version_id='v1.0', project_id='123', path='token')
    params = {
        'api_key': '456',
        'action': 'read',
    }
    headers = {
        'Accept': 'application/json'
    }
    res = dummy_app.get(url, params, headers, status=200)
    assert 200 == res.status_code


def test_routing_to_humans_txt(dummy_app):
    res = dummy_app.get('/humans.txt', status=200)
    assert 200 == res.status_code


def test_routing_to_robots_txt(dummy_app):
    res = dummy_app.get('/robots.txt', status=200)
    assert 200 == res.status_code
