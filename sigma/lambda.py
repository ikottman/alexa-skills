import boto3
import os

sqs = boto3.client('sqs')
queue = os.environ['queue']

def send_message(message):
    sqs.send_message(QueueUrl=queue, MessageBody=message)

def turn_tv_on():
    send_message('on')

def turn_tv_off():
    send_message('off')

def lambda_handler(event, context):
    # parse the intent
    state = event['request']['intent']['slots']['state']['value']

    if state == 'on':
        turn_tv_on()
        message = 'Turning TV on.'
    else:
        turn_tv_off()
        message = 'Turning TV off.'

    # return the response
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': message
            }
        }
    }
