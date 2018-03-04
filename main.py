# Name: main.py
# Author: Robin Goyal
# Last-Modified: March 4, 2018
# Purpose: Count the number of words in a reddit post

import praw
from bs4 import BeautifulSoup


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

    #####################
    # Need to call submission.title before printing vars(submission) to
    # view all of the individual attributes of the submission instance
    # - Title of post is in submission.title
    # - Body of post is in submission.selftext
    #   - Parse body text using beautiful soup
    # - Comments are in self.comments
    #   - Will need to use the MoreComments object to access
    #     each reply to the comments

    # Get title
    title = submission.title

    # Extract text from html formatted body
    soup = BeautifulSoup(submission.selftext, 'html.parser')
    body = soup.get_text().split()

    # Printing out comments
    for top_level_comment in submission.comments:
        # Encounters MoreComments error if post includes load more comments button
        # Need to use the MoreComments model from praw to overcome this error
        print(top_level_comment.body)

    # Print title and body
    print(title)
    print(body)


def main():
    get_post("https://www.reddit.com/r/books/comments/81v3g1/what_phrase_in_a_book_description_will_ensure_you/")


if __name__ == "__main__":
    main()
