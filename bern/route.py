import pyramid.httpexceptions as exc

from bern.service import IValidator


def authentication_predicator(info, req):
    """Validates `project_id` and `api_key` using AuthenticationValidator."""
    route_name = info.get('route', {}).name
    valid_routes = (
        'issue_token',
    )
    if route_name in valid_routes:
        match = info.get('match')
        if 'api_key' not in req.params or not match:
            raise exc.HTTPForbidden()

        project_id = match.get('project_id')
        api_key = req.params.get('api_key')
        action = req.params.get('action')

        validator = req.find_service(iface=IValidator, name='authentication')
        if not validator.validate(project_id=project_id, api_key=api_key,
                                  action=action):
            raise exc.HTTPNotAcceptable()

        return True

    return False


def includeme(config):
    # v1.0
    config.add_route(
        'issue_token',
        '/v1.0/projects/{project_id}/credentials/token',
        custom_predicates=(authentication_predicator,)
    )
