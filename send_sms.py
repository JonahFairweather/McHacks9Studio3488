from twilio.rest import Client
import praw
import os

# using the praw library and a script created using the reddit api we are able to use our local host to webscrape reddit
# this creates a Reddit instance
reddit = praw.Reddit(
    client_id="3YhYN_v6icb9G4RZmqHnyw",
    client_secret="hxNP6hdsr9O37akYy_da7ArV79tPKQ",
    user_agent="SubScraper"
)

# for adding to the final message
prompt = ""

def get_prompt():
    global prompt
    # finds the days top rated post in r/WritingPrompts and returns it as a PRAW Subreddit instance
    top = reddit.subreddit('WritingPrompts').top("day", limit=1)
    for post in top:
        # trims off the standard header used i r/WritingPrompts
        prompt = post.title[5::]
    return prompt


print(get_prompt())

# See Environment Variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# creates and instance of Client from the twilio library
client = Client(account_sid, auth_token)

# sends message to our client
message = client.messages \
    .create(
    body=prompt,
    from_='+16067312179',
    to='+12023049104'
)

# to ensure we have sent the message correctly we print out the ID which can be verified on the Twilio platform
print(message.sid)
