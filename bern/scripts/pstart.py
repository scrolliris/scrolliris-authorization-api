import os
import sys

from pyramid.paster import (
    get_app,
    setup_logging
)

from bern.env import Env


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s {staging|production}.ini")' % (cmd, cmd))
    sys.exit(1)


def wsgi_app(argv=None):
    from bern.env import load_dotenv_vars

    if not argv:
        argv = sys.argv

    if len(argv) < 2:
        usage(argv)

    load_dotenv_vars()

    config_uri = argv[1] if 1 in argv else 'config/production.ini'
    app = get_app(config_uri, 'bern')
    setup_logging(config_uri)

    return app


def main(argv=None):
    import cherrypy

    app = wsgi_app(argv)

    # pylint: disable=invalid-name
    cherrypy.tree.graft(app, '/')
    cherrypy.server.unsubscribe()

    env = Env()
    server = cherrypy._cpserver.Server()  # pylint: disable=protected-access
    server.socket_host = env.host
    server.socket_port = env.port
    server.thread_pool = 30
    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    sys.exit(main(sys.argv) or 0)
