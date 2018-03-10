# Name: submission.py
# Author: Robin Goyal
# Last-Modified: March 10, 2018
# Purpose: Class representing a reddit submission


import praw
from datetime import datetime


class Submission(object):
    """
    A class which creates a dictionary for frequent words in submission.

    Note:
        The Submission object does not account for mispelled words and
        only accounts for words in the English language.

    Attributes:
        id: id of submission
        title: title of the submission
        subreddit_id: id of the subreddit the submission belongs to
        last_request: the most recent date the submission was accessed
        comments: an instance of praws CommentForest model for all comments
        body: body of the submission
    """

    def __init__(self, url, reddit=None):
        """
        Args:
            url: url of submission
            reddit: instance of reddits python wrapper API
        """

        if reddit is None:
            reddit = praw.Reddit()

        # To-Do: Handle an invalid URL at the Submission level
        try:
            submission = reddit.submission(url=url)
        except praw.exceptions.ClientException:
            print("Not a valid url")

        # Initialize submission attributes
        self.title = submission.title
        self.id = submission.id
        self.subreddit_id = submission.subreddit_id
        self.comments = submission.comments
        self.last_request = datetime.now()
        self.body = submission.selftext_html

    def get_freq_dict(self):
        """
        (Submission) -> dict: (str, int)

        Returns a dictionary containing the 15 most frequent words
        in a reddit submission ignoring common English words.
        """

        pass

    def update_dict(dict, string):
        """
        (dict: (str, int), str) -> (dict: (str, int))

        Update dict from the frequency of words in string.

        Example:
        >>> dict = {"the": 2, "bird": 3}
        >>> update_freq_dict(dict, "the bird is red")
        >>> dict
        {"the": 3, "bird": 4, "is": 1, "red": 1}
        """

        pass

    def parse_string(string):
        """
        (str) -> list: str

        Returns a list of lowercase words from string after
        parsing punctuation and whitespace.

        Example:
        >>> parse_string("It's the first day of the\n New Year")
        ["its", "the", "first", "day", "of", "the", "new", "year"]
        """

        pass

    def filter_common_words(dict):
        """
        (dict: (str, int)) -> (dict: (str, int))

        Returns a dictionary with common english words filtered
        from dict as specified by nltk.corpus.stopwords.words.

        Example:
        >>> filter_common_words({"blue": 3, "the": 2, "sky": 3, "is": 1})
        {"blue": 3, "sky": 3}
        """

        pass

    def get_top_words(dict):
        """
        (dict: (str, int)) -> (dict: (str, int))

        Returns a dictionary containing the 15 most frequent
        words from dict and the remaining word frequencies
        summed as a single key known as "others". Original
        dictionary is returned if less than 15 words.
        """

        pass
