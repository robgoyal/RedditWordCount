# Name: main.py
# Author: Robin Goyal
# Last-Modified: March 4, 2018
# Purpose: Count the number of words in a reddit post

import praw
from bs4 import BeautifulSoup
# import string
import re


def get_reddit_instance():
    """
    (file) -> praw.Reddit

    Returns a praw.Reddit instance to make requests
    to Reddit's API with configuration information
    from praw.ini.
    """

    return praw.Reddit(site_name="WordCountBot")


def get_post(url):

    # Reddit instance
    reddit = get_reddit_instance()

    # Get reddit post
    submission = reddit.submission(url=url)

    # Get title
    title = submission.title

    # Extract text from html formatted body
    soup = BeautifulSoup(submission.selftext, 'html.parser')
    body = soup.get_text()

    # Get all comments (nested and MoreComments) in post
    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()

    # Remove all punctuation except for words and spaces
    regex = r'[^\w\s]|_'

    # List function obtains all nested comments as well
    for i, comment in enumerate(all_comments):
        # filtered_string = top_level_comment.body.translate(translator)
        s = re.sub(regex, '', comment.body)
        print(s.split())

    # Print title and body
    print(title)
    print(body)


# def parse_str(string)


def main():
    get_post("https://www.reddit.com/r/books/comments/822jin/reading_has_helped_me_take_my_mind_off_of_my/")


if __name__ == "__main__":
    main()
