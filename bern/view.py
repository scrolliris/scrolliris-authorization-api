import json

from pyramid.response import Response
from pyramid.view import (
    forbidden_view_config,
    notfound_view_config,
    view_config,
)
import pyramid.httpexceptions as exc

from bern import logger


def no_cache(_request, response):
    response.pragma = 'no-cache'
    response.expires = '0'
    response.cache_control = 'no-cache,no-store,must-revalidate'


def includeme(_config):
    pass


# -- errors

@notfound_view_config(renderer='json',
                      append_slash=exc.HTTPMovedPermanently)
def notfound(req):
    req.response.status = 404
    return dict()


@forbidden_view_config(renderer='json')
def forbidden(req):
    req.response.status = 403
    return dict()


@view_config(context=exc.HTTPInternalServerError, renderer='string')
def internal_server_error(req):
    body = 'Cannot {} {}'.format(req.method, req.path)
    return Response(body, status='500 Internal Server Error')


# -- actions

@view_config(route_name='issue_token',
             renderer='json',
             request_method='OPTIONS')
def issue_token_option(req):
    """Returns empty response with header informations for OPTIONS request."""
    prefix = req.env.get('RESPONSE_PREFIX', '')
    res = Response(prefix + json.dumps({}), status='200 OK')

    res.headers['Access-Control-Max-Age'] = '600'
    res.headers['Access-Control-Expose-Headers'] = \
        'Cache-Control,Content-Language,Content-Type,Expires,Last-Modified,' \
        'Pragma'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = \
        'Content-Type,X-Requested-With,X-CSRF-Token'
    res.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET'

    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Content-Encoding'] = 'identity'
    res.headers['X-Content-Type-Options'] = 'nosniff'
    return res


@view_config(route_name='issue_token',
             renderer='json',
             request_method='GET')
def issue_token(req):
    """Returns an issued token."""
    if 'api_key' not in req.params:
        raise exc.HTTPForbidden()

    if str(req.accept).lower() != 'application/json':
        raise exc.HTTPNotFound()

    # TODO
    # project_id = req.matchdict.get('project_id')
    # api_key = req.params.get('api_key')
    # action = req.params.get('action')

    req.add_response_callback(no_cache)

    result = {}
    logger.info(result)

    prefix = req.env.get('RESPONSE_PREFIX', '')
    res = Response(prefix + json.dumps(dict(result)), status='200 OK')

    res.headers['Access-Control-Allow-Origin'] = '*'

    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Content-Encoding'] = 'identity'
    res.headers['X-Content-Type-Options'] = 'nosniff'
    return res
