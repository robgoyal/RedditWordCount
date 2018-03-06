# Name: main.py
# Author: Robin Goyal
# Last-Modified: March 4, 2018
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

    # Reddit instance
    reddit = get_reddit_instance()

    # Get reddit post
    submission = reddit.submission(url=url)

    return submission


def get_freq_dict(submission):

    # Initialize dictionary
    words_frequency = {}
    total_words = 0

    # Remove all punctuation except for words and spaces
    regex = r'[^\w\s]|_'

    # Update dictionary with title frequency
    title = re.sub(regex, '', submission.title)
    total_words += update_frequency(words_frequency, title)

    # Update dictionary with body frequency
    soup = BeautifulSoup(submission.selftext, 'html.parser')
    body = re.sub(regex, '', soup.get_text())
    total_words += update_frequency(words_frequency, body)

    # Update dictionary with all comments
    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()

    for comment in all_comments:
        comment = re.sub(regex, '', comment.body)
        total_words += update_frequency(words_frequency, comment)

    return total_words, words_frequency


def update_frequency(d, string):
    num_words = 0
    for word in string.split():
        word = word.lower()
        num_words += 1
        if word in d:
            d[word] += 1
        else:
            d[word] = 1

    return num_words


def main():
    submission = get_post("https://www.reddit.com/r/funny/comments/82ckwf/pic_of_two_plump_pigeons_perched_on_the_ledge_but/")

    total_words, words_frequency = get_freq_dict(submission)

    print(total_words)
    for k in sorted(words_frequency, key=words_frequency.get, reverse=True)[0:20]:
        print(k, words_frequency[k])


if __name__ == "__main__":
    main()
