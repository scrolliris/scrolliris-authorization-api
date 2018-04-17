# pylint: disable=redefined-outer-name,unused-argument
from __future__ import absolute_import
import os

import pytest
from pyramid import testing
from pyramid.paster import get_appsettings
from pyramid_services import find_service
from webtest.app import TestApp
from zope.interface.adapter import AdapterRegistry

from bern import main
from bern.env import Env, load_dotenv_vars


# NOTE:
# The request variable in py.test is special context of testing.
# See http://doc.pytest.org/en/latest/fixture.html#request-context

TEST_DIR = os.path.dirname(__file__)
INI_FILE = os.path.join(TEST_DIR, '..', 'config', 'testing.ini')


@pytest.fixture(scope='session')
def dotenv():  # type () -> None
    # same as bern:main
    dotenv_file = os.path.join(TEST_DIR, '..', '.env')
    load_dotenv_vars(dotenv_file)
    return


@pytest.fixture(scope='session')
def env(dotenv):  # type (None) -> dict
    return Env()


@pytest.fixture(scope='session')
def raw_settings(dotenv):  # type(None) -> dict
    return get_appsettings('{0:s}#{1:s}'.format(INI_FILE, 'bern'))


@pytest.fixture(scope='session')
def resolve_settings():  # type () -> function
    def _resolve_settings(raw_s):
        return raw_s

    return _resolve_settings


@pytest.fixture(scope='session')
def settings(raw_settings, resolve_settings):
    # type (dict, function)-> dict
    return resolve_settings(raw_settings)


@pytest.fixture(scope='session')
def extra_environ(env):  # type (Env) -> dict
    environ = {
        'SERVER_PORT': '80',
        'REMOTE_ADDR': '127.0.0.1',
        'wsgi.url_scheme': 'http',
    }
    return environ


@pytest.yield_fixture(autouse=True, scope='session')
def session_helper():  # type () -> None
    yield


@pytest.yield_fixture(autouse=True, scope='module')
def module_helper(settings):  # type () -> None
    yield


@pytest.yield_fixture(autouse=True, scope='function')
def function_helper():  # type () -> None
    yield


@pytest.fixture(scope='session')
def config(request, settings):
    # type (Router, dict) -> Configurator
    config = testing.setUp(settings=settings)

    config.include('bern.route')

    def teardown():  # type () -> None
        testing.tearDown()

    request.addfinalizer(teardown)

    return config


@pytest.fixture(scope='function')
def dummy_request(extra_environ):  # type (dict) -> Request
    locale_name = 'en'
    req = testing.DummyRequest(
        subdomain='',
        environ=extra_environ,
        _LOCALE_=locale_name,
        locale_name=locale_name,
        matched_route=None)

    # for service objects
    req.service_cache = AdapterRegistry()
    req.find_service = (lambda *args, **kwargs:
                        find_service(req, *args, **kwargs))
    return req


@pytest.fixture(scope='session')
def _app(raw_settings):  # type (dict) -> Router
    global_config = {
        '__file__': INI_FILE
    }
    if '__file__' in raw_settings:
        del raw_settings['__file__']

    return main(global_config, **raw_settings)


@pytest.fixture(scope='session')
def dummy_app(_app, extra_environ):  # type (Router, dict) -> TestApp
    app = TestApp(_app, extra_environ=extra_environ)
    req = app.RequestClass
    req.find_service = (lambda *args, **kwargs:
                        find_service(req, *args, **kwargs))
    return app
