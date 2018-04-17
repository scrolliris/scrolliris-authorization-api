import sys

from bern.env import load_dotenv_vars


def main(argv=None, quiet=False):
    """Runs original pserve with .env support."""
    # NOTE:
    # `pserve` (PServeCommand) needs `hupper`, it has dependency to **fcntl**.
    # In some environment (e.g. appengine), fcntl is not found :'(
    # So, that's why this import is in method.
    from pyramid.scripts.pserve import PServeCommand

    if not argv:
        argv = sys.argv
    load_dotenv_vars()

    command = PServeCommand(argv, quiet=quiet)
    return command.run()


if __name__ == '__main__':
    sys.exit(main() or 0)
