from flask import Flask, request
import requests
import json

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAB0zOeDA58cBO0zbyIEZA2wsjnHSBCZBTjE57ZB2lI09C9ivJOkKG2TU9v2B7KvrLMsGnaVKDeBMRnfcwYzk6x41JVtQR4aZCCrGTVfKTqwfCpnZCUstgHJ6r4glOXOPEnrJKeLAYm77bEYRyt71J7mNYu8ZCgBmjuVwkA2byUjUIUjgkPveC2gY9A5bDezx81ywZDZD'
#VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'
VERIFY_TOKEN = 'my_verify_token_12345'

@app.route('/', methods=['GET'])
def verify():     
    print('All parameters:', request.args.to_dict())
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Verification failed'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']

                    reply_message(sender_id, message_text)
    return 'OK', 200

def reply_message(sender_id, message_text):
    response = {
        'recipient': {'id': sender_id},
        'message': {'text': f'You said: {message_text}'}
    }
    headers = {'Content-Type': 'application/json'}
    url = f'https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    requests.post(url, headers=headers, data=json.dumps(response))

if __name__ == '__main__':
    #app.run(port=5000)
    app.run()

