import requests
from watsonAssistant import callWatsonAssistantAPI

# for fb messager
PAGE_ACCESS_TOKEN = 'EAAPUUreSpHoBAJ3WoDBDGp9TJTFzTTZA5gJG8G24VrqgWJYGZBMmf8PNPm2VuDdnoRzI5zWIZBn2cHk30exBb7wSZCwzR7e3nScna5PzQgiDc3VMIVrMSRaEVWy0dHwOizHmlimVqZA2y9vf41pqJAW2V8b0KMwefPzuSlxk7KAZDZD'

# Handles messages events
def handleMessage(sender_psid, received_message):
    # Check if the message contains text
    if received_message['text']:
        user_input = received_message['text']
        context = {}
        action = ''

        assistent = callWatsonAssistantAPI(user_input, context)
        context = assistent['context']

        if 'action' in assistent['output']:
            current_action = assistent['output']['action']
            # if current_action == 'display_time':

        # Create the payload for a basic text message
        response = {
            "text": assistent['output']['text'][0]
        }

    # Sends the response message
    callSendAPI(sender_psid, response)

# Handles messaging_postbacks events
def handlePostback(sender_psid, received_postback):
    print('hola')

# Sends response messages via the Send API
def callSendAPI(sender_psid, response):
    # Construct the message body
    request_body = {
        "recipient": {
            "id": sender_psid
        },
        "message": response
    }

    # # Send the HTTP request to the Messenger Platform
    url = "https://graph.facebook.com/v2.6/me/messages"
    params = {'access_token':PAGE_ACCESS_TOKEN}

    r = requests.post(url, params=params, json=request_body)

    print(r.status_code)
    print(r.json)