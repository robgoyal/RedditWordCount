# Name: helpers.py
# Author: Robin Goyal
# Last-Modified: March 7, 2018
# Purpose: Helper functions for the application


from bs4 import BeautifulSoup
import re
import praw
from nltk.corpus import stopwords


def get_reddit_instance():
    """
    (file) -> praw.Reddit

    Returns a praw.Reddit instance to make requests
    to Reddit's API with configuration information
    from praw.ini.
    """

    return praw.Reddit(site_name="WordCountBot")


def get_freq_dict(submission, d={}):
    """
    (praw.Reddit.Submission) -> dict: (str: int)

    Returns a dictionary containing the frequency
    of words from a submission's title, body and comments.
    """

    words_frequency = d.copy()

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
    (dict: (str: int), str)

    Update dictionary, d with the frequency of
    each word in string.
    """

    # Split string at all whitespace
    for word in string.split():

        # Lowercase word for consistency
        word = word.lower()

        # Increment frequency of word if exists in d
        d[word] = d.get(word, 0) + 1


def clean_dict(d):
    """
    (dict) -> dict

    Remove common english words from dictionary
    """
    regex = r'[^\w\s]|_'
    common_words = [re.sub(regex, '', word) for word in stopwords.words('english')]

    filtered_dict = {word: d[word] for word in d if word not in common_words}

    return filtered_dict
