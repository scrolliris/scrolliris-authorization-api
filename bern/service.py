# pylint: disable=inherit-non-class,no-self-argument,no-method-argument
from __future__ import absolute_import
import sys

from zope.interface import Interface

from bern import logger


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


def includeme(config):
    config.register_service_factory(
        authentication_validator_factory(),
        iface=IValidator,
        name='authentication')
