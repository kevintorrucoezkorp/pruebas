
import json
import boto3


class SQSQueue(object):
    def __init__(self,queueName=None):
        self.resource = boto3.resource('sqs')
        self.queue = self.resource.get_queue_by_name(QueueName=queueName)
        self.QueueName= queueName

    def send(self,Message={},MessageGroupId={}):
        print("Hola2")
        data= json.dumps(Message)
        reponse=self.queue.send_message(MessageBody=data,MessageGroupId='120')
        return reponse
    def received(self):
        try:
            queue=self.resource.get_queue_by_name(QueueName=self.QueueName)
            for message in queue.received_messages():
                data=message.body
                data = json.loads(data)
                message.delete()
        except Exception:
            print(Exception)
            return[]
        return data
