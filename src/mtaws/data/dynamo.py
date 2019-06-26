from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, UTCDateTimeAttribute,
                                 MapAttribute, ListAttribute, BooleanAttribute,
                                 JSONAttribute, NumberAttribute)
from pynamodb.indexes import (GlobalSecondaryIndex, AllProjection,
                              KeysOnlyProjection, IncludeProjection)
import os
import uuid
from datetime import datetime
from mtaws.constants import AWS_REGION

DDB_HOST = None
if os.environ.get("DDB_HOST"):
    DDB_HOST = os.environ.get("DDB_HOST")

# define table names
ACCOUNTS_TBL = os.environ.get("ACCOUNTS_TBL", "accounts")

class Account(Model):

    class Meta:
        table_name = ACCOUNTS_TBL
        host = DDB_HOST
        region = AWS_REGION
        write_capacity_units = 10
        read_capacity_units = 10

    id = UnicodeAttribute(hash_key=True)
    created = UTCDateTimeAttribute(default=datetime.utcnow())
    name = UnicodeAttribute()
    aws_account_id = UnicodeAttribute(null=True)
    secondary_emails = ListAttribute()
    create_state = UnicodeAttribute()
    account_type = UnicodeAttribute()



    #GSI's

