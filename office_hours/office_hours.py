# allows modules to be imported from the ./dependencies directory
import sys
sys.path.insert(0, './dependencies')

# for calling external APIs
import requests
import json

# for handling KMS secret decryption
import os
import boto3
from base64 import b64decode

# get and decode secrets from KMS
ENCRYPTED_KEY = os.environ['google_api_key']
ENCRYPTEED_LOCATION = os.environ['location']
GOOGLE_API_KEY = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_KEY))['Plaintext']
LOCATION = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTEED_LOCATION))['Plaintext']

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print("intent name was: " + intent_name)

    if intent_name == "Place":
        return Maps.is_place_open(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "To see if a business is open, say: ask office hours if Taco Bell is open."

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Sorry, I didn't understand what you said."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


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

class Maps:

    @staticmethod
    def is_place_open(intent):
        # call google places to find the nearest location for the search
        print(intent)
        place = intent['slots']['name']['value']

        # search for the place name within a 50,000 meter (roughly 31 mile) radius of the specified gps coordinates.
        api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + \
                  LOCATION + "&name=" + place + "&rankby=distance&key=" + GOOGLE_API_KEY

        response = requests.get(api_url)
        speech_output = "Sorry, couldn't find anything for " + place
        if response is not None and response.content is not None and response.status_code == 200:
            json_response = json.loads(response.content)
            if len(json_response['results']) > 0:
                result = json_response['results'][0]
                if result['opening_hours']['open_now']:
                    speech_output = result['name'] + " at " + result['vicinity'] + " is open."
                else:
                    speech_output = result['name'] + " at " + result['vicinity'] + " is closed."
        return build_response({}, build_speechlet_response(title=intent['name'],
                                                           output=speech_output,
                                                           reprompt_text="Please try again.",
                                                           should_end_session=True))
