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
    state = event['request']['intent']['slots']['state']['value']
    if state == 'on':
        turn_tv_on()
        message = 'Turned on tv.'
    else:
        turn_tv_off()
        message = 'Turned off tv.'

    # return the response
    speech = build_speechlet_response('Sigma', message, '', True)
    response = build_response({}, speech)
    return response

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
