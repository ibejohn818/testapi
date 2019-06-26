import boto3
from mtaws.constants import (
    AWS_REGION,
    SQS_ENDPOINT
)

class SqsClient:
    """
    """

    _client = None

    def __init__(self, queue_url, queue_name,  receipt=None):
        self.queue_url = queue_url
        self.queue_name = queue_name
        self.receipt = receipt
        self._resource = None


    def client(self):
        """ Create, cache and return
            an sqs boto client
        """
        if not self._client:
            self._client = boto3.client('sqs',
                                        endpoint_url=SQS_ENDPOINT,
                                        region_name=AWS_REGION)
        return self._client

    def resource(self):
        """
        """
        if not self._resource:
            self._resource = boto3.resource('sqs',
                                            endpoint_url=SQS_ENDPOINT,
                                            region_name=AWS_REGION).Queue(self.queue_url)
        return self._resource

    def add(self, body, **kw):
        """
        """
        payload = {
            'MessageBody': body,
            'QueueUrl': self.queue_url,
            'MessageAttributes': {}
        }

        payload.update(kw)

        # add queue name attribute
        payload['MessageAttributes'].update({
            'QueueName': {
                'DataType': 'String',
                'StringValue': self.queue_name
            }
        })

        return self.client().send_message(**payload)


    def visibility_timeout(self, sec=360):
        """ Set the refresh timeout to
            reprocess this message later

        Args:
            set (int): Number of seconds to set refresh timeout
        """
        return self.client().change_message_visibility(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=self.receipt,
                    VisibilityTimeout=sec)

    def delete(self):
        """ Delete the sqs message
        """
        return self.client().delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=self.receipt)

    def execute(self, msg):
        """ Stub method that the queue runner
            will execute
        """
        raise Exception("execute method must be implemented")


