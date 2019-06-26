import os
import boto3
from mtaws.data import sqs

def handler(evt, ctx):
    """ Handle incoming sqs messages
    """

    if len(evt.get("Records", [])) <= 0:
        exit(0)

    for record in evt.get("Records"):
        try:
            receipt = record.get('receiptHandle')
            attr = record.get('messageAttributes')
            queue_name = attr.get('QueueName').get('stringValue')

            # get an sqs instance
            queue = sqs.Sqs.factory(queue_name, receipt)
            # execute
            queue.execute(record)


        except Exception as e:
            # alert of error via SNS Topic
            print("SQS HANDLER EXCEPTION: ", str(e))
