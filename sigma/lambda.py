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

def turn_volume_up():
    send_message('up')

def turn_volume_down():
    send_message('down')

def lambda_handler(event, context):
    # parse the intent
    if 'value' in event['request']['intent']['slots']['power']:
        power = event['request']['intent']['slots']['power']['value']
        if power == 'on':
            turn_tv_on()
            message = 'Turning TV on.'
        elif power == 'off':
            turn_tv_off()
            message = 'Turning TV off.'
    elif 'value' in event['request']['intent']['slots']['volume']:
        volume = event['request']['intent']['slots']['volume']['value']
        if volume == 'up':
            turn_volume_up()
            message = 'Turning volume up.'
        elif volume == 'down':
            turn_volume_down()
            message = 'Turning volume down.'
    else:
        message = "Sorry I don't understand"

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
