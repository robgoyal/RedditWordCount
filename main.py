# Name: main.py
# Author: Robin Goyal
# Last-Modified: March 6, 2018
# Purpose: Count the number of words in a reddit post

import praw
from bs4 import BeautifulSoup
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
    """
    (str) -> praw.Reddit.Submission

    Returns an instance of the Submission object
    from reddits API which contains information
    for a submission from url.
    """

    # Reddit instance
    reddit = get_reddit_instance()

    # Get reddit post
    submission = reddit.submission(url=url)

    return submission


def get_freq_dict(submission):
    """
    (praw.Reddit.Submission) -> dict: (str, int)

    Returns a dictionary containing the frequency
    of words from a submission's title, body and comments.
    """

    words_frequency = {}

    # Remove all punctuation except for words and spaces
    regex = r'[^\w\s]|_'

    # Update words frequency dictionary from title
    title = re.sub(regex, '', submission.title)
    update_frequency(words_frequency, title)

    # Update words frequency dictionary from body
    soup = BeautifulSoup(submission.selftext, 'html.parser')

    # Remove html formatting from body
    body = re.sub(regex, '', soup.get_text())
    update_frequency(words_frequency, body)

    # Update words frequency from all comments
    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()

    for comment in all_comments:

        # Replace punctuation from comments body
        comment = re.sub(regex, '', comment.body)
        update_frequency(words_frequency, comment)

    return words_frequency


def update_frequency(d, string):
    """
    (dict: (str, int), str)

    Update dictionary, d with the frequency of
    each word in string.
    """

    # Split string at all whitespace
    for word in string.split():

        # Lowercase word for consistency
        word = word.lower()

        # Increment frequency of word if exists in d
        d[word] = d.get(word, 0) + 1


def main():

    # Get total number of words and frequency of words in submission
    post_url = input("URL of post submission: ")
    submission = get_post(post_url)
    words_frequency = get_freq_dict(submission)
    total_words = sum(words_frequency.values())

    # Print out information
    print(total_words)
    for k in sorted(words_frequency, key=words_frequency.get, reverse=True)[0:20]:
        print(k, words_frequency[k])


if __name__ == "__main__":
    main()
