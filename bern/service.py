# pylint: disable=inherit-non-class,no-self-argument,no-method-argument
from __future__ import absolute_import
import base64
import sys
import uuid

import redis
from zope.interface import Interface

from bern import logger


# -- validator

class IValidator(Interface):
    # pylint: disable=missing-docstring

    def validate():
        pass


class AuthenticationValidator(object):
    """A service which checks the validity of request with credentials."""

    def __init__(self, *_args, **_kwargs):
        if sys.version_info[0] > 3:
            # pylint: disable=missing-super-argument
            super().__init__()
        else:
            super(AuthenticationValidator, self).__init__()

    # pylint: disable=no-self-use
    def validate(self, project_id='', api_key='', action='read'):
        """Validates params (project_access_key_id and api_key)."""
        logger.info('project_id -> %s, api_key -> %s, action -> %s',
                    project_id, api_key, action)

        return True


def authentication_validator_factory():
    def _authentication_validator(_, req):
        return AuthenticationValidator(req)

    return _authentication_validator


# -- generator

class IGenerator(Interface):
    # pylint: disable=missing-docstring

    def generate():
        pass


class TokenGenerator(object):
    """Token generator."""

    def __init__(self, *_args, **_kwargs):
        self.redis = None

        if sys.version_info[0] > 3:
            # pylint: disable=missing-super-argument
            super().__init__()
        else:
            super(TokenGenerator, self).__init__()

    @staticmethod
    def generate_token():
        return base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8')

    def generate(self, project_id='', api_key='', action='read'):
        """Generates new token."""
        logger.info('project_id: %s, api_key: %s, action: %s',
                    project_id, api_key, action)

        token = self.__class__.generate_token()
        logger.info('token: %s', token)

        # TODO
        _data = {
            'token': token,
            'project_id': project_id,
            'api_key': api_key,
            'action': action,
            'generated_at': ''
        }

        return token


def token_generator_factory():
    def _token_generator(_, req):
        generator = TokenGenerator(req)

        settings = req.settings
        generator.redis = redis.Redis(
            settings.get('queue_url', 'redis://localhost:6379/0')
        )
        return generator

    return _token_generator


def includeme(config):
    config.register_service_factory(
        authentication_validator_factory(),
        iface=IValidator, name='authentication')

    config.register_service_factory(
        token_generator_factory(),
        iface=IGenerator, name='token')
