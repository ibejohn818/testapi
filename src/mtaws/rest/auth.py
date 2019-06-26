from flask import request
from flask_restplus import abort
from functools import wraps
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class apikeyauth:

    def chk_api_key_header(self):
        """
        """
        if 'X-API-KEY' in request.headers:
            return True

        return False

    def auth_api_key(self):
        """
        """
        # get the api key from aws secret manager
        # or use a jwt or something, ENV is
        # just for dev :-)

        API_KEY=os.environ.get("SWAGG_API_KEY")

        if API_KEY is None:
            # get the API_KEY from somewhere else
            # ^^ read above
            logger.info("WE DID NOTHING")

        key = request.headers.get('X-API-Key')

        if key == API_KEY:
            return True

        return False

    def __call__(self, fn):
        @wraps(fn)
        def auth(*a, **k):
            if not self.chk_api_key_header():
                abort(401, message='API Key Missing', error='AUTH REQUIRED')

            if not self.auth_api_key():
                abort(403, message="Not Authorized", error='ACCESS DENIED')

            return fn(*a, **k)

        return auth
