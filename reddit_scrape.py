import praw
import os
from praw.models import MoreComments, Comment


reddit = praw.Reddit(
    client_id="3YhYN_v6icb9G4RZmqHnyw",
    client_secret="hxNP6hdsr9O37akYy_da7ArV79tPKQ",
    user_agent="SubScraper"
)


def find_top_post():
    # finds the top rated post for the day
    top_post = reddit.subreddit('WritingPrompts').top("day", limit=1)
    return top_post


def get_prompt():
    prompt = ""
    # finds the days top rated post in r/WritingPrompts and returns it as a PRAW Subreddit instance
    top = reddit.subreddit('WritingPrompts').top("month", limit=1)
    for post in top:
        # trims off the standard header used i r/WritingPrompts
        prompt = post.title[5::]
    return prompt


def top_url():
    # find the URL of the top post
    # This is a field of the ListingGenerator class instance we are working with (loops for ease)
    url = ""
    hot_posts = find_top_post()
    for post in hot_posts:
        url = post.url
    return url


def extract_comments():
    url = top_url()
    # creates an instance of the Submission class
    submission = reddit.submission(url=url)
    comment_content = ""
    # looping through the root comments of the resulting comment trees
    for root_comment in submission.comments:
        # will come across MoreComments (tags such as "load more comments") we want to skip these
        if isinstance(root_comment, MoreComments):
            continue
        # we want to ignore the AutoModerator comments so we check the author of Comment instances
        if isinstance(root_comment, Comment) and root_comment.author == "AutoModerator":
            continue
        comment_content += root_comment.body
    return comment_content


if __name__ != '__main__':
    posts = find_top_post()


if __name__ == '__main__':
    print("test")
