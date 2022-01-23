from datetime import datetime

from twilio.rest import Client
import praw
import os
import reddit_scrape

# using the praw library and a script created using the reddit api we are able to use our local host to webscrape reddit
# this creates a Reddit instance
reddit = praw.Reddit(
    client_id="3YhYN_v6icb9G4RZmqHnyw",
    client_secret="hxNP6hdsr9O37akYy_da7ArV79tPKQ",
    user_agent="SubScraper"
)

prompt = reddit_scrape.get_prompt()
# See Environment Variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# creates and instance of Client from the twilio library
client = Client(account_sid, auth_token)


def send_prompt():
    p = reddit_scrape.get_prompt()
    full_prompt = "Take some time to reflect with Bubble at .\nHere is your prompt for today:\n" + p
    # sends message to our client
    message = client.messages \
        .create(
            body=full_prompt,
            messaging_service_sid='MG1803e16098d246e86ee09763272fb28d',
            to='+12023049104'
        )
    return message


def send_reminder():
    message = client.messages \
        .create(
            messaging_service_sid='MG1803e16098d246e86ee09763272fb28d',
            body='REMINDER: Let your creativity flow with Bubble.\nRemember to submit your journal entry on our' +
                 'website: ',
            to='+12023049104'
        )
    return message


message = send_prompt()
# to ensure we have sent the message correctly we print out the ID which can be verified on the Twilio platform
print(message.sid)
