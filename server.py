from __future__ import print_function
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask, request, make_response, abort
from fbHandlesMessage import handleMessage as fbhmsg, handlePostback as fbhpb
from telegramHandlesMessage import handleMessage as tghmsg

my_token = 'token_webhook_test_watsonassistent'

# Flask app should start in global layout
app = Flask(__name__)

# VALIDAR LAS APP CONECTADAS
@app.route('/fb/webhook', methods=['GET', 'POST'])
def fbWebhook():
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge', '')
        token = request.args.get('hub.verify_token', '')
        mode = request.args.get('hub.mode', '')
        if mode and token:
            if mode == 'subscribe' and token == my_token:
                print('WEBHOOK_VERIFIED')
                return make_response(challenge, 200)
            else:
                print('WEBHOOK_NOT_VERIFIED')
        return  make_response('GET sin parametros', 403)

    elif request.method == 'POST':
        req = request.get_json(silent=True, force=True)
        print("Request:")
        print(json.dumps(req, indent=4))

        # Check the webhook event is from a Page subscription
        if req['object'] == 'page':

            # Iterate over each entry - there may be multiple if batched
            for entry in req['entry']:

                # Get the webhook event. entry.messaging is an array, but
                # will only ever contain one event, so we get index 0
                if 'messaging' in entry:
                    webhook_event = entry['messaging'][0]
                    print('messaging:')
                    print(json.dumps(webhook_event, indent=4))
                else:
                    continue


                # Get the sender PSID
                sender_psid = webhook_event['sender']['id']
                print('Sender PSID:')
                print(sender_psid)

                # Check if the event is a message or postback and
                # pass the event to the appropriate handler function
                if webhook_event['message']:
                    fbhmsg(sender_psid, webhook_event['message'])
                elif webhook_event['postback']:
                    fbhpb(sender_psid, webhook_event['postback'])


        return make_response('EVENT_RECEIVED', 200)

    else:
        return  make_response('EVENT_NOT_RECEIVED', 403)

@app.route('/telegram/webhook', methods=['GET', 'POST'])
def telegramWebhook():
    token = request.args.get('hub.verify_token', '')
    if token == my_token:
        req = request.get_json(silent=True, force=True)
        print("Request:")
        print(json.dumps(req, indent=4))
        if  'message' in req:
            print('message:')
            print(json.dumps(req['message'], indent=4))
            chat_id = req['message']['chat']['id']
            print('chat_id: ')
            print(chat_id)
            tghmsg(chat_id, req['message'])

        return make_response('EVENT_RECEIVED', 200)

    else:
        return  make_response('EVENT_NOT_RECEIVED', 403)

@app.route('/teams/webhook', methods=['GET', 'POST'])
def teamsWebhook():
    req = request.get_json(silent=True, force=True)
    
    print("Request:")
    print(request.method)
    print(request.headers)
    print(json.dumps(req, indent=4))
       
    #token = request.args.get('hub.verify_token', '')
    #return make_response('EVENT_RECEIVED', 200)
    return make_response("{\"type\": \"message\",\"text\":\"Hola, soy el bot1!\"}", 200)
     

@app.route('/test', methods=['GET'])
def test():
    return  "Bienvenido Prueba Team RPA !!"


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')