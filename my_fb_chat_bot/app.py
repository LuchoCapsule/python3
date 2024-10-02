from flask import Flask, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# According your chatbot configuration in Facebook Developer Portal you will have to change the values of the following variables
PAGE_ACCESS_TOKEN = 'EAAV3tdotiQ4BOxEtfbMV9ngrUBdVSZCkixtJVm0l6oOJttXQI9YuuKNIGZAWxV2tBUfyBlLTNVkzmOEZAR5tu8MGcZCZCkdZA2RCgTVp9GSwnFuUBnNaLibjDAwLyMYoQ2mZCnaw7uZBv9wlzp0xi7CZB1ZCYbaWWHy5MvFJfJqjdSIhtvI2rWZCnHxfymw9tQh9CJy2QZDZD'
# Verify Token is a random string that you define. It is used to validate the authenticity of the request from Facebook
# when you set up your webhook. You can set it to any value you like.
VERIFY_TOKEN = 'my_verify_token_12345'

@app.route('/', methods=['GET'])
def verify():     
    print('All parameters:', request.args.to_dict())
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Verification failed 123'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            print('Entry:', entry)
            for messaging_event in entry['messaging']:
                print('Messaging event:', messaging_event)
                if messaging_event.get('message'):
                    print('Message:', messaging_event['message'])
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    print('Sender ID:', sender_id)
                    print('Message text:', message_text)
                    reply_message(sender_id, message_text)
    return 'OK', 200

def reply_message(sender_id, message_text):
    response = {
        'recipient': {'id': sender_id},
        'message': {'text': f'You said: {message_text}'}
    }
    print('Response:', response)
    headers = {'Content-Type': 'application/json'}
    url = f'https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    requests.post(url, headers=headers, data=json.dumps(response))

if __name__ == '__main__':
    #app.run(port=5000)
    app.run()