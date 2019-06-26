from flask_restplus import fields
from mtaws.rest.api import api


err_msg = api.model('error_msg', {
    'message': fields.String(readonly=True, description='Description or error'),
    'error': fields.String(readonly=True, description='Details about the error'),
})

paginated = api.model('paginated', {
    'pages': fields.Integer(description='Number of pages'),
    'page': fields.Integer(description='Current page number'),
    'total': fields.Integer(description='Total number of records'),
    'limit': fields.Integer(description='Total records in page')

})

account = api.model('account', {
    'id': fields.String(readonly=True, description='Account Primary Key UUID'),
    'aws_account_id': fields.Integer(readonly=True, description='AWS Account ID'),
    'name': fields.String(description='Name of account'),
    'create_state': fields.String(readonly=True, description='The creation state of the account. Starts at "PENDING" ends at "COMPLETED"'),
    'account_type': fields.String(description='The type of account. Choices: managed, hostops, system'),
    'active': fields.Boolean(readonly=True, description='If account is active'),
    'root_email': fields.String(readonly=True, description='Email address of the root user'),
    'secondary_emails': fields.List(fields.String(description='Secondary email address'), description='List of secondary email addresses')
})

account_list = api.inherit('account_list', paginated, {
    'accounts': fields.List(fields.Nested(account))
})

account_create_state = api.model('account_create_state', {
    'name': fields.String(readonly=True, description='The name of the state'),
    'description': fields.String(readonly=True, description='An explanation of the states context')
})
account_create_state_list = api.model('account_create_state_list', {
    'states': fields.List(fields.Nested(account_create_state))
})
