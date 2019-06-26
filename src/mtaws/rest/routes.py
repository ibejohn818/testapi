

def route_api_namespaces(restplus_api):
    """ Import and route the restplus
        api namespaces/resources

    Args:
        restplus_api (:obj:`flask_restplus.Api`): The restplus Api in-scope
    """
    from mtaws.rest.endpoints.onboarding.accounts import ns as accounts_ns
    from mtaws.rest.endpoints.lightsail.instance import ns as lightsail_ns

    restplus_api.add_namespace(accounts_ns)
    restplus_api.add_namespace(lightsail_ns)
