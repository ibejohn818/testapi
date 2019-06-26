import os
import sys
import json
from enum import Enum
import boto3
from importlib import import_module
from mtaws.data import queues


class QueueUrls(Enum):
    OnboardAccounts=os.environ.get("SQS_ONBOARD_ACCOUNTS",
                              "http://sqs:9324/queue/OnboardAccounts")
class Sqs:

    @classmethod
    def factory(cls, queue_or_url, receipt=None):
        """ Create and return a SqsClient instance from
            the QueueUrls enum name or value

        Args:
            queue_or_url (str): The QueueUrls enum name or value
            receipt (str): The sqs messages receipt_handle

        Returns:
            (:obj:`.Sqs`): An Sqs instance
        """
        queue = None

        if hasattr(QueueUrls, str(queue_or_url)):
            queue = getattr(QueueUrls, queue_or_url)
        else:
            try:
                queue = QueueUrls(str(queue_or_url))
            except Exception as e:
                pass

        if not queue:
            raise Exception("Queue doesn't exist: {}".format(
                queue_or_url))

        if hasattr(queues, queue.name):
            obj = getattr(queues, queue.name)
        else:
            obj = cls

        new = obj(queue.value,
                queue.name,
                receipt)

        return new
