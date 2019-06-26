import os

SQS_ENDPOINT=None
if os.environ.get("DOCKER"):
    SQS_ENDPOINT="http://sqs:9324"

AWS_REGION=os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
