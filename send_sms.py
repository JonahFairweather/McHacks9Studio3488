import os
from twilio.rest import Client

# See Environment Variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Test",
                     from_='+16067312179',
                     to='+12023049104'
                 )

print(message.sid)