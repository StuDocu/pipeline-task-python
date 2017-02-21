import boto3
from os.path import join, dirname
from dotenv import load_dotenv
from Task import *

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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