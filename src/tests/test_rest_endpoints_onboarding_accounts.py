import pytest
from pytest_mock import mocker
from flask import url_for
import os
from mtaws import app
from .utils import TestClient

@pytest.fixture
def client():
    client = TestClient()
    return client

class TestAccounts:

    uri = "/onboarding/accounts"


    def test_get_401(self, client, mocker):
        """ test 401
            IE: no api key
        """
        res = client.get(self.uri, auth=False)

        assert res.status_code == 401
        assert res.data.decode().strip() ==\
            '{"error": "AUTH REQUIRED", "message": "API Key Missing"}'

    def test_get_403(self, client, mocker):
        """ test 403
            Wrong api key
        """
        res = client.get(self.uri, auth=False, headers={
            'X-API-KEY': '321'
        })

        assert res.status_code == 403
        assert res.data.decode().strip() ==\
            '{"error": "ACCESS DENIED", "message": "Not Authorized"}'

    def test_get_200(self, client, mocker):
        """
        """
        pass

    # test post method

    @pytest.fixture
    def new_account(self):
        """
        """
        return {
            "name": "Test Name",
            "secondary_emails": [
                "test@test.com",
                "mock@mock.com"
            ]
        }

    def test_post_401(self, client, new_account):
        """ test 401
            IE: no api key
        """
        import json
        res = client.post(self.uri, auth=False,
                        data=new_account)

        assert res.status_code == 401
        assert res.data.decode().strip() ==\
            '{"error": "AUTH REQUIRED", "message": "API Key Missing"}'

    def test_post_403(self, client, new_account):
        """ test 403
            Wrong api key
        """
        res = client.post(self.uri, auth=False, headers={
            'X-API-KEY': '321'
        },data=new_account)

        assert res.status_code == 403
        assert res.data.decode().strip() ==\
            '{"error": "ACCESS DENIED", "message": "Not Authorized"}'

    def test_post_200(self, client, new_account):
        """
        """
        res = client.post(self.uri, data=new_account)
        print(res.__dict__)
        print(res.data)

class TestAccountsCreateStates:

    uri = "/onboarding/accounts/create-states"

    def test_401(self, client, mocker):
        """ test 401
            IE: no api key
        """
        res = client.get(self.uri, auth=False)

        assert res.status_code == 401
        assert res.data.decode().strip() ==\
            '{"error": "AUTH REQUIRED", "message": "API Key Missing"}'

    def test_403(self, client, mocker):
        """ test 403
            Wrong api key
        """
        res = client.get(self.uri, auth=False, headers={
            'X-API-KEY': '321'
        })

        assert res.status_code == 403
        assert res.data.decode().strip() ==\
            '{"error": "ACCESS DENIED", "message": "Not Authorized"}'

    def test_200(self, client, mocker):
        """
        """
        # patch controller
        ctlr = mocker.patch('mtaws.rest.endpoints.onboarding.accounts.accounts')
        ctlr.list_account_create_states.return_value = [{
            'name': 'test-name',
            'description': 'test-description'
        }]
        res = client.get(self.uri)

        assert res.status_code == 200
        assert res.data.decode().strip() == ('{"states": [{"name": '
                                    '"test-name", "description": '
                                    '"test-description"}]}')
