from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from dispatcher import MessageHandler, ResponseType

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
async def bot():
    message = request.values.get('Body', '')
    sender = request.values.get('From', '')

    messageHandler = MessageHandler()
    response = await messageHandler.handle(message, sender)

    resp = MessagingResponse()
    msg = resp.message()

    msg.body(response['body'])
    if (response['media'] is not None):
        msg.media(response['media'])

    return str(resp)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('static/images', path)


@app.route('/')
def index():
    return "É isso aqui x 3!"


if __name__ == '__main__':
    app.run()
