import os
import json
from mtaws import app

class TestClient:

    _client = None

    def _mock(self, method, url, **kw):
        """ Mock the flask client with
            option to send api-key
        """

        if self._client is None:
            os.environ['SWAGG_API_KEY'] = '123'
            app.app.config['TESTING'] = True
            self._client = app.app.test_client()

        params = {
            'auth': True,
            'headers': {
                'content-type': 'application/json'
            }
        }

        # merge header dict
        if kw.get('headers') and \
                isinstance(kw.get('headers'), dict):
            params['headers'].update(kw['headers'])
            del kw['headers']

        params.update(kw)

        if params.get('auth'):
            params['headers']['X-API-KEY'] = '123'

        # remove auth setting
        del params['auth']

        if isinstance(params.get('data'), dict):
            params['data'] = json.dumps(params['data'])

        return getattr(self._client, method)(url, **params)



    def __getattr__(self, name, *args, **kw):
        """
        """
        def _catch(*args, **kw):
            return self._mock(name, *args, **kw)
        return _catch
