import sys
import os
from flask import request
from flask_restplus import abort, Resource
from flask_restplus.errors import ValidationError
from mtaws.rest.api import api
from mtaws.rest.auth import apikeyauth
from mtaws.rest.endpoints.serializers import (
    account,
    account_list,
    account_create_state,
    account_create_state_list,
    paginated,
    err_msg
)
from mtaws.controllers.onboarding.accounts import Account


ns = api.namespace('onboarding',
                   description='Onboarding operations on accounts',
                   )

@api.response(401, "Auth Error", err_msg)
@api.response(403, "Access Denied", err_msg)
@ns.route('/accounts')
class Accounts(Resource):

    @api.marshal_with(account_list)
    @apikeyauth()
    def get(self):
        """ Get a list of accounts in the MT Aws org
        """
        return {
            'page': 1,
            'pages': 10,
            'total': 20,
            'limit': 30,
            'accounts':[{ 'id': 'test', 'name': 'test name'}]
        }

    @api.expect(account)
    @api.marshal_with(account)
    @api.response(200, 'Account Queued For Create', account)
    @api.response(400, 'Validation Error', err_msg)
    @apikeyauth()
    def post(self, **kw):
        """ Create a new Aws account in the MT Aws Org
        """
        try:
            result = Account.create(api.payload)
        except ValidationError as ve:
            abort(400, "Validation Error", errors=ve.msg)
        except Exception as e:
            abort(500, "internal error")

        return result

@api.response(401, "Auth Error", err_msg)
@api.response(403, "Access Denied", err_msg)
@ns.route('/accounts/<string:id>')
class AccountsEdit(Resource):

    @api.marshal_with(account)
    @api.response(404, "Account not found", err_msg)
    @apikeyauth()
    def get(self, id):
        """ Get account by id
        """
        acc = Account.get_by_id(id)
        if not acc:
            abort(404, "Account not found")
        return acc

    @api.expect(account)
    @apikeyauth()
    def put(self, id):
        """ Edit account
        """
        return {}, 201

    @api.expect(account)
    @apikeyauth()
    def delete(self, id):
        """ Delete account
        """
        return {}, 204

@api.response(401, "Auth Error", err_msg)
@api.response(403, "Access Denied", err_msg)
@ns.route('/accounts/create-states')
class AccountCreateStates(Resource):

    @api.marshal_with(account_create_state_list)
    @apikeyauth()
    def get(self):
        """ Return a list of all possible Account
            create_states with descriptions
        """
        cs = Account.list_create_states()
        return {'states': cs}, 200
