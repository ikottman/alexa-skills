import boto3
import os
import time
import logging
from subprocess import call

# setup client for connecting to the queue
# pull the url from the environment variable sqs_queue
sqs = boto3.client('sqs')
queue_url = os.environ['sqs_queue']

# setup logger
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def delete_message(receipt):
  sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)

def turn_tv_on():
  logging.info('turning on')
  call("echo 'on 0' | cec-client -s -d 1 RPI", shell=True)

def turn_tv_off():
  logging.info('turning off')
  call("echo 'standby 0' | cec-client -s -d 1 RPI", shell=True)

def poll_queue():
  messages = sqs.receive_message(QueueUrl=queue_url)

  if ('Messages' in messages):
    body = messages['Messages'][0]['Body']
    receipt = messages['Messages'][0]['ReceiptHandle']

    if (body == 'on'):
      turn_tv_on();
    elif (body == 'off'):
      turn_tv_off();
    else:
      logging.error('found invalid message body', body)

    # delete the message so we don't get it again
    delete_message(receipt)


# poll for messages every five seconds. Ignore failures
while True:
  try:
    poll_queue()
  except Exception as e:
    logging.error(e)
  time.sleep(5)
