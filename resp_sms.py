from flask import Flask, request
from twilio import twiml

# allows us to receive the message then respond in a dynamic way

app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form["From"]
    message_body = request.form["Body"]
    print(message_body)
    print(number)

    resp = twiml.Response()
    resp.message("Hello {}, you said {}".format(number, message_body))
    return str(resp)


if __name__ == '__main__':
    app.run()