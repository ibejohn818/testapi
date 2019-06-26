import json
from mtaws.data.queues.client import SqsClient

class OnboardAccounts(SqsClient):

    def queue_account_create(self, acc_dict):
        """
        """
        payload = {
            'MessageAttributes': {
                'SomeKey': {
                    'DataType': 'String',
                    'StringValue': 'Some Value'
                }
            }
        }
        return self.add(json.dumps(acc_dict), **payload)

    def execute(self, msg):
        """
        """
        # check how many times we've processed this message
        print("MESSAGE")
        print(msg)
        tries =  int(msg.get('attributes').get('ApproximateReceiveCount'))
        print("ATTEMPT: {}".format(tries))
        if tries > 5:
            # send a message to somebody then delete
            print("DELETING")
            self.delete()
        else:
            # retry in 2 min
            print("RETRY IN 30 SECONDS")
            self.visibility_timeout(30)

