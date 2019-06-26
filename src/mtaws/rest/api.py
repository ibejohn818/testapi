import os
from flask_restplus import Api
from flask import (
    Blueprint,
    url_for,
    request
)
from flask_restplus import apidoc
from mtaws import __version__

api = Api(version=__version__,
            title='MT AWS Api',
            description='Api interface for MT AWS operations',
            authorizations = {
                'apikey': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'X-API-KEY'
                }
            },
          security='apikey',
          doc='/swagger-ui'
          )



def route_swagger_assets(flask_app, uri):
    """ Change the routing
        which swagger assets
        are served from

    Args:
        flask_app (:obj:`flask.Flask`): The flask app in-scope
        uri (str): The uri to serve assets from (Start path with forward slash / )
    """

    custom_apidoc = apidoc.Apidoc('restplus_custom_doc', __name__,
                                template_folder='templates',
                                static_folder=os.path.dirname(apidoc.__file__) + '/static',
                                static_url_path='/swaggerui')

    @custom_apidoc.add_app_template_global
    def swagger_static(filename):
        return url_for('restplus_custom_doc.static',
                    filename=filename)

    flask_app.register_blueprint(custom_apidoc, url_prefix=uri)


# register exception handler
@api.errorhandler
def error_500(e):
    """ Exception catch all
    """
    msg = {'message':
            'Unhandled error occurred'}

    return msg, 500


