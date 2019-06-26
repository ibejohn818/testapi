import json
from mtaws.data.queues.client import SqsClient

class OnboardAccounts(SqsClient):

    def queue_account_create(self, acc_dict):
        """
        """
        return self.add(json.dumps(acc_dict))

    def execute(self, msg):
        """
        """
        print("IN EXE")
        print(msg)
        self.visibility_timeout(20)
        print("MESSAGE REQUEUED!")

