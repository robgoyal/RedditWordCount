# Name: main.py
# Author: Robin Goyal
# Last-Modified: March 3, 2018
# Purpose: Count the number of words in a reddit post

import praw


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

def main():
    get_post("https://www.reddit.com/r/leafs/comments/81s050/maple_leafscapitals_outdoor_game_proceeding_as/")


if __name__ == "__main__":
    main()
