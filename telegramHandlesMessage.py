import requests
from watsonAssistant import callWatsonAssistantAPI

# for telegram token
PAGE_ACCESS_TOKEN = '600453224:AAFaiVOinDHPyPoW1RSQhQNCe7JIECtQYnI'

# Handles messages events
def handleMessage(chat_id, received_message):
    # Check if the message contains text
    if 'text' in received_message:
        user_input = received_message['text']
        context = {}
        action = ''

        assistent = callWatsonAssistantAPI(user_input, context)
        context = assistent['context']

        if 'action' in assistent['output']:
            current_action = assistent['output']['action']
            # if current_action == 'display_time':

        # Create the payload for a basic text message
        response = assistent['output']['text'][0]

    # Sends the response message
    callSendAPI(chat_id, response)

# Sends response messages via the Send API
def callSendAPI(chat_id, response):
    # Construct the message body
    request_body = {
        "chat_id": chat_id,
        "text": response
    }

    # # Send the HTTP request to the Messenger Platform
    url = "https://api.telegram.org/bot" + PAGE_ACCESS_TOKEN + "/sendmessage"

    r = requests.post(url, json=request_body)

    print(r.status_code)
    print(r.json)
    