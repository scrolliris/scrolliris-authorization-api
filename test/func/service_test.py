import pytest

import redis

from bern.service import (
    IGenerator,
    IValidator,
    TokenGenerator,
    AuthenticationValidator,
)


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):
    # pylint: disable=unused-argument
    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_service_findability(monkeypatch, dummy_request):
    validator = dummy_request.find_service(iface=IValidator,
                                           name='authentication')
    assert isinstance(validator, AuthenticationValidator)

    class DummyRedis(object):
        def __init__(self, *args, **kwargs):
            pass

    monkeypatch.setattr(redis, 'Redis', DummyRedis)

    generator = dummy_request.find_service(iface=IGenerator, name='token')
    assert isinstance(generator, TokenGenerator)
