from mtaws.data import dynamo
from mtaws.data import models
import uuid
from datetime import datetime
from enum import Enum
from mtaws.data import sqs
import json

class OrmBase:
    """ Base class of an ORM Object
    """
    dynamo = None

class Accounts(OrmBase):
    dynamo = dynamo.Account

    class CreateStates(Enum):
        pending='pending'
        completed='completed'
        error='error'


    def __init__(self):
        self.create_state_descriptions = {
            self.CreateStates.pending: "Account registered and pending creation",
            self.CreateStates.completed: "",
            self.CreateStates.error: "",
        }

    def list_create_states(self):
        """
        """
        s = []
        for cs in self.CreateStates:
            s.append({
                'name': cs.value,
                'description': self.create_state_descriptions[cs]
            })
        return s

    def get_by_id(self, id):
        """
        """
        try:
            result = self.dynamo.query(id)
            for acc in result:
                return acc
        except Exception as e:

            print(str(e))

        return False


    def create_from_api(self, data={}):
        """
        """
        new = self.dynamo(
            id=str(uuid.uuid4()),
            name=data.get('name'),
            secondary_emails=data.get('secondary_emails'),
            create_state=self.CreateStates.pending.value
        )
        if not new.save():
            raise Exception("Error saving new account")

        # queue account create
        schema = models.AccountSchema()
        payload, _ = schema.dumps(new)
        sqs.Sqs.factory("OnboardAccounts").queue_account_create(payload)

        return new
