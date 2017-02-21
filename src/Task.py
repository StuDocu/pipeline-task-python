import boto3
import json
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

class Task:
    def __init__(self, sqs, task_id, handle):
        if not callable(handle):
            raise Exception("`handle` must be callable")

        self.sqs = sqs
        self.id = task_id
        self.queue = self.sqs.create_queue(QueueName=self.id)
        self.handle = handle
        # self.queue = sqs.get_queue_by_name(QueueName=self.id)

    def listen(self):
        messages = self.sqs.receive_message(QueueUrl=self.queue["QueueUrl"], WaitTimeSeconds=20, MaxNumberOfMessages=10)
        for message in messages.get('Messages'):
            body = message["Body"]
            self.sqs.delete_message(QueueUrl=self.queue["QueueUrl"], ReceiptHandle=message["ReceiptHandle"])
            self.run(body)

    def run(self, body):
        body = json.loads(body)
        result = self.handle(body["payload"])
        pipeline_id = body["pipeline_id"]
        pipeline_url = body["pipeline"]

        self.done(pipeline_id, pipeline_url, result)

    def done(self, pipeline_id, pipeline_url, payload):
        self.sqs.send_message(
            QueueUrl = pipeline_url,
            MessageBody = json.dumps({
                'completed': self.id,
                'payload': payload,
                'pipeline_id': pipeline_id,
                'status': 'success',
                'type':'task-completed',
            }),
            DelaySeconds=0
        )

sqs = boto3.client(
    'sqs',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=environ.get('SQS_AWS_REGION')
)

def bla(ponies):
    return "yeaaaah boyyyyyyyyyyyyyyyy"

t = Task(sqs, 'task_poniardos', bla)
t.listen()