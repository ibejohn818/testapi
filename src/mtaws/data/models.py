from datetime import (
    date,
    datetime
)
from marshmallow import (
    Schema,
    fields,
    pprint,
    post_load
)
import uuid


class AccountSchema(Schema):

    id = fields.UUID()
    name = fields.String(required=True)
    create_state = fields.String()
    aws_account_id = fields.String()
    active = fields.Boolean()
    secondary_emails = fields.List(fields.Email())

