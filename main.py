# Name: main.py
# Author: Robin Goyal
# Last-Modified: March 7, 2018
# Purpose: Calculate the frequency of words in reddit post(s)

from helpers import *


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


def get_subreddit(subreddit):
    """
    (praw.models.Subreddit) -> dict: (str: int)

    Count the frequency of words in posts
    from subreddit within the past day.
    """

    reddit = get_reddit_instance()
    submissions = reddit.subreddit(subreddit).top('day')

    frequency = {}

    for submission in submissions:
        frequency = get_freq_dict(submission, frequency)
        # print(frequency)

    frequency = clean_dict(frequency)
    return frequency


def main():

    # Get total number of words and frequency of words in submission
    # post_url = input("URL of post submission: ")
    # submission = get_post(post_url)
    # words_frequency = get_freq_dict(submission)
    # total_words = sum(words_frequency.values())

    freq = get_subreddit('learnprogramming')
    total_words = sum(freq.values())

    # Print out information
    print(total_words)
    for k in sorted(freq, key=freq.get, reverse=True)[0:20]:
        print(k, freq[k])

    return freq


if __name__ == "__main__":
    main()
