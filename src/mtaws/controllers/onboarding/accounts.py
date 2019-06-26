from mtaws.data import orm
from mtaws.data import models
from flask_restplus.errors import ValidationError



class Account:

    @classmethod
    def create(cls, data):
        """
        """
        err = cls.validate_create(data)

        if len(err.keys()) > 0:
            raise ValidationError(err)

        acc = orm.Accounts()

        result = acc.create_from_api(data)

        return result

    @classmethod
    def get_by_id(cls, id):
        """
        """
        acc = orm.Accounts()
        result = acc.get_by_id(id)
        return result

    @staticmethod
    def validate_create(data):
        """
        """
        schema = models.AccountSchema()

        res = schema.validate(data, partial=('create_state',
                                             'aws_account_id',
                                             'active'))

        return res

    @staticmethod
    def list_create_states():
        """
        """
        a = orm.Accounts()
        return a.list_create_states()
