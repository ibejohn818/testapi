import os
import sys
from flask import (Flask, Blueprint, jsonify)
from flask_cors import CORS
from mtaws.rest.api import (
    api,
    route_swagger_assets
)
from mtaws.rest.routes import route_api_namespaces

app = Flask(__name__)

# enable cross site
CORS(app, resources={"*": {"origins": "*"}})

# config # move to something better
# IE: py files or datastore
DEBUG=False
ENV='production'
API_PREFIX=os.environ.get("API_PREFIX", "")

if os.environ.get("DOCKER"):
    DEBUG=True
    ENV='development'

app.config['RESTPLUS_VALIDATE'] = True
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['FLASK_ENV'] = ENV
app.config['DEBUG'] = DEBUG

# wrap restplus Api in blueprint
# so we can control the prefix
api_bp = Blueprint('Api',
                   __name__,
                   url_prefix=API_PREFIX)

# init restplus API
api.init_app(api_bp)

# add endpoint namespaces
route_api_namespaces(api)

# register api'ified blueprint w/flask app
app.register_blueprint(api_bp)

# route swagger assets
route_swagger_assets(app, "{}/swagger-ui".format(API_PREFIX))

@app.before_request
def app_before_request():
    """ Handle things like auth
        or block the swagger-ui
    """
    pass


if __name__ == '__main__':
    app.run(debug=True)
