from flask import Flask, request, Response
from twilio import twiml
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

# allows us to receive the message then respond in a dynamic way

app = Flask(__name__)


@app.route('/sms', methods=['POST', "GET"])
def sms():
    message_body = request.form.get("Body")
    resp = MessagingResponse()

    resp.message("Hello back to you!")
    return Response(str(resp), mimetype="application/xml"), 200


if __name__ == '__main__':
    app.run(debug=True)
