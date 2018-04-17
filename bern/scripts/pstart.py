from __future__ import absolute_import, print_function
import os
import sys

from pyramid.paster import (
    get_app,
    setup_logging
)

from bern.env import Env, load_dotenv_vars


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s {staging|production}.ini")' % (cmd, cmd))
    sys.exit(1)


def wsgi_app(argv=None):
    if not argv:
        argv = sys.argv

    if len(argv) < 2:
        usage(argv)

    load_dotenv_vars()

    config_uri = argv[1] if 1 in argv else 'config/production.ini'
    setup_logging(config_uri)

    app = get_app(config_uri, 'bern')
    return app


def main(argv=None):
    import cherrypy  # only for production
    app = wsgi_app(argv)

    env = Env()
    # pylint: disable=invalid-name
    cherrypy.tree.graft(app, '/')
    cherrypy.log.error_log.propagate = False
    cherrypy.server.unsubscribe()

    print('server.socket_host: {}'.format(env.host))
    print('server.socket_port: {}'.format(env.port))

    cherrypy.config.update({
        'server.socket_host': env.host,
        'server.socket_port': env.port,
        'engine.autoreload.on': False,
    })
    server = cherrypy._cpserver.Server()  # pylint: disable=protected-access
    server.socket_host = env.host
    server.socket_port = env.port
    server.thread_pool = 30
    server.subscribe()

    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    sys.exit(main(sys.argv) or 0)
