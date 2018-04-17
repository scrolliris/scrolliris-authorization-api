from __future__ import absolute_import
import logging
import socket
from os import path
import sys
import types
from wsgiref.handlers import BaseHandler

from pyramid.config import Configurator
from pyramid.threadlocal import get_current_registry

from bern.env import Env
from bern.request import Request

# -- configurations

STATIC_DIR = path.join(path.dirname(path.abspath(__file__)), '../static')


# pylint: disable=protected-access
def ignore_broken_pipes(self):
    """Ignores unused error message about broken pipe."""
    try:
        ex = BrokenPipeError
    except NameError:
        ex = socket.error
    if sys.exc_info()[0] != ex:
        BaseHandler.__handle_error_original_(self)


BaseHandler.__handle_error_original_ = BaseHandler.handle_error
BaseHandler.handle_error = ignore_broken_pipes
# pylint: enable=protected-access

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(sh)
# pylint: enable=invalid-name


def get_settings():
    return get_current_registry().settings


def get_expected_env_value_from(env, key, expected_type):
    """Get value(s) through environment variable."""
    value = env.get(key, None)
    if not isinstance(value, expected_type):
        return None
    # split, but ignore empty string
    if ',' in value:
        value = [v for v in value.split(',') if v != '']
    return value


def resolve_env_vars(settings):
    env = Env()
    s = settings.copy()

    string_type = str
    if sys.version_info[0] < 3:
        try:
            # `types.StringTypes` works also in Python2.7's unicode
            string_type = types.StringTypes
        except AttributeError:
            pass

    for k, k_upper in Env.settings_mappings().items():
        # ignores missing key or it has a already value in config
        if k not in s or s[k]:
            continue
        new_v = get_expected_env_value_from(env, k_upper, string_type)
        if new_v:
            s[k] = new_v
    return s


def main(_, **settings):
    config = Configurator(settings=resolve_env_vars(settings))
    config.set_request_factory(Request)

    # routes
    # static files at /*
    filenames = [f for f in ('robots.txt', 'humans.txt')
                 if path.isfile((STATIC_DIR + '/{}').format(f))]
    if filenames:
        env = Env()
        cache_max_age = 3600 if env.is_production else 0
        config.add_asset_views(
            STATIC_DIR, filenames=filenames, http_cache=cache_max_age)

    config.scan()

    config.include('.service')
    config.include('.route')
    config.include('.view')

    app = config.make_wsgi_app()
    # from paste.translogger import TransLogger
    # app = TransLogger(app, setup_console_handler=False)
    return app
