import pytest

import redis

from bern.service import (
    AuthenticationValidator,
    authentication_validator_factory,
    TokenGenerator,
    token_generator_factory,
)


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):
    # pylint: disable=unused-argument
    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_authentication_validator_initalization(dummy_request):
    validator = AuthenticationValidator()
    assert isinstance(validator, AuthenticationValidator)

    factory = authentication_validator_factory()
    validator = factory({}, dummy_request)
    assert isinstance(validator, AuthenticationValidator)


def test_authentication_validator():
    validator = AuthenticationValidator()
    assert validator.validate()


def test_token_generator_initalization(monkeypatch, dummy_request):
    generator = TokenGenerator()
    assert isinstance(generator, TokenGenerator)

    class DummyRedis(object):
        def __init__(self, *args, **kwargs):
            pass

    monkeypatch.setattr(redis, 'Redis', DummyRedis)

    factory = token_generator_factory()
    generator = factory({}, dummy_request)
    assert isinstance(generator, TokenGenerator)


def test_token_generator(monkeypatch, dummy_request):
    class DummyRedis(object):
        def __init__(self, *args, **kwargs):
            pass

    monkeypatch.setattr(redis, 'Redis', DummyRedis)

    factory = token_generator_factory()
    generator = factory({}, dummy_request)
    assert generator.generate()
