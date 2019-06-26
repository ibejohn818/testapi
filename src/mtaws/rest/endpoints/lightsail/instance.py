from flask import request
from flask_restplus import (abort, Resource)
from mtaws.rest.api import api
from mtaws.rest.endpoints.serializers import (
    account,
    err_msg
)
from mtaws.rest.endpoints.lightsail.serializers import (
    lightsail_instance,
    lightsail_instance_list
)
from mtaws.rest.auth import apikeyauth
import sys
import os

ns = api.namespace('lightsail',
                   description='Control customer lightsail')


@api.response(401, "Auth Error", err_msg)
@api.response(403, "Access Denied", err_msg)
@ns.route('/<int:account_id>/instances')
class LighsailCustomer(Resource):

    @api.marshal_with(lightsail_instance_list)
    @apikeyauth()
    def get(self, account_id):
        """ List customers lightsail instances
        """
        return {}, 200

    @api.expect(lightsail_instance)
    @apikeyauth()
    def post(self, account_id):
        """ Create a lightsail instance
            under the customer account
        """
        return {}, 201

@api.response(401, "Auth Error", err_msg)
@api.response(403, "Access Denied", err_msg)
@ns.route('/<int:account_id>/instance/<int:lightsail_id>')
class LightsailInstance(Resource):

    @api.marshal_with(lightsail_instance)
    @apikeyauth()
    def get(self, account_id, lightsail_id):
        """ Get lighsail instance
        """
        return {}

    @api.expect(lightsail_instance)
    @apikeyauth()
    def put(self, account_id, lightsail_id):
        """ Edit customer lightsail instance
        """
        return {}, 204

    @api.expect(lightsail_instance)
    @apikeyauth()
    def delete(self, account_id, lightsail_id):
        """ Delete customer lightsail instance
        """
        return {}, 204

