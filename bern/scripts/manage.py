from __future__ import absolute_import, print_function
import os
import sys

from pyramid.paster import setup_logging
# from pyramid.scripts.common import parse_vars

from bern.env import load_dotenv_vars


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <command> <action> [var=value]\n'
          '(example: "%s \'development.ini#\' ...")' % (cmd, cmd))
    sys.exit(1)


def main(argv=None):
    if not argv:
        argv = sys.argv

    if len(argv) != 4:
        usage(argv)

    config_uri = argv[1]
    # command = argv[2]
    # action = argv[3]
    # options = parse_vars(argv[4:])

    setup_logging(config_uri)

    load_dotenv_vars()

    raise Exception('Not implemented yet')
