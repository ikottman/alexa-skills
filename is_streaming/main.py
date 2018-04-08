# allows modules to be imported from the ./dependencies directory
import sys
sys.path.insert(0, './dependencies')

# for calling external APIs
import requests
import json

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

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

    if intent_name == "streamers":
        return get_response()
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
    speech_output = "To hear what's streaming on Twitch, say 'what is live right now?'"

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

def get_response():
    streamers = get_followed_streamers()
    names = keep_live_users(streamers)

    speech_output = ''
    if (len(streamers) == 0):
        speech_output = 'No one is streaming right now.'
    else:
        speech_output = ' and'.join(names) + ' are streaming right now.'

    return build_response({}, build_speechlet_response(title='Streamers',
                                                       output=speech_output,
                                                       reprompt_text="Please try again.",
                                                       should_end_session=True))

# takes in [(user id, display name)]
# returns list of users currently streaming
def keep_live_users(streamers):
    ids = [ streamer[0] for streamer in streamers ]
    
    headers = { 'Client-ID': 'fb8brzjsgp1lsl7vnj6clt4ozvuz8c' }
    url = 'https://api.twitch.tv/helix/streams?user_id=' + '&user_id='.join(ids)
    response = requests.get(url)
    
    live_ids = []
    if response.status_code == 200:
        json_response = json.loads(response.content)
        live_ids = [ stream.user_id for stream in json_response['data'] ]

    return [ streamer[1] for streamer in streamers if streamer[0] in live_ids ]

# returns list of tuples of people we follow
def get_followed_streamers():
    headers = { 'Client-ID': 'fb8brzjsgp1lsl7vnj6clt4ozvuz8c' }
    url = 'https://api.twitch.tv/helix/users/follows?from_id=167211639'
    response = requests.get(url)
    
    usernames = []
    if response.status_code == 200:
        json_response = json.loads(response.content)
        usernames = [ (follow.id, follow.display_name) for follow in json_response['data'] ]
    
    return usernames