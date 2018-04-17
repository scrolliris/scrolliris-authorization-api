import sys

from pyramid.request import Request as OriginalRequest

from bern.env import Env

__all__ = ['Request']


class Request(OriginalRequest):  # pylint: disable=too-many-ancestors
    def __init__(self, *args, **kwargs):
        # There is already `self.environ` in request env.
        # But, the `environ` is os's environ (wrapper)
        # This is our Env instance.
        self.env = Env()

        if sys.version_info[0] > 3:
            # pylint: disable=missing-super-argument
            super().__init__(*args, **kwargs)
        else:
            super(Request, self).__init__(*args, **kwargs)

    @property
    def settings(self):
        from bern import get_settings
        return get_settings() or {}
