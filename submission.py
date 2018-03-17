# Name: submission.py
# Author: Robin Goyal
# Last-Modified: March 17, 2018
# Purpose: Class representing a reddit submission


import praw
from datetime import datetime
import bs4
import re
from nltk.corpus import stopwords


def update(d, string):
    """
    (dict: (str, int), str))

    Update dictionary d from the frequency of words in string.

    Example:
    >>> d = {"the": 2, "bird": 3}
    >>> update(d, "the bird is red")
    >>> d
    {"the": 3, "bird": 4, "is": 1, "red": 1}
    """

    # List of parsed words
    parsed_words = parse(string)

    for word in parsed_words:

        # Lowercase word for consistency in dictionary
        word = word.lower()
        d[word] = d.get(word, 0) + 1


def parse(string):
    """
    (str) -> list: str

    Returns a list of lowercase words from string after
    parsing punctuation and whitespace.

    Example:
    >>> parse_string("It's the first day of the\n New Year")
    ["its", "the", "first", "day", "of", "the", "new", "year"]
    """

    # Apply regular expression to string
    regex = r'[^\w\s]|_'
    words = re.sub(regex, '', string)

    # Return a list with whitespace removed
    return words.split()


def filter_common_words(d):
    """
    (dict: (str, int)) -> (dict: (str, int))

    Returns a dictionary with common english words filtered
    from d as specified by nltk.corpus.stopwords.words.

    Example:
    >>> filter_common_words({"blue": 3, "the": 2, "sky": 3, "is": 1})
    {"blue": 3, "sky": 3}
    """

    d = d.copy()

    common_words = parse(" ".join(stopwords.words('english')))

    filtered_d = {word: d[word] for word in d if word not in common_words}

    return filtered_d


def get_top_words(frequency):
    """
    (dict: (str, int)) -> (dict: (str, int))

    Returns a dictionary containing the 15 most frequent
    words from dict and the remaining word frequencies
    summed as a single key known as "__others". Original
    dictionary is returned if less than 20 words.
    """

    # Create dictionary with top 20 words
    sorted_frequency = sorted(frequency, key=frequency.get, reverse=True)
    d = {k: frequency[k] for k in sorted_frequency[:20]}

    # Create key for remaining words in frequency dictionary
    if len(frequency) > 20:
        d["__other"] = sum(frequency[k] for k in sorted_frequency[20:])

    return d


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
        self.frequency = {}
        self.total_words = None

        # Retrieve all comments from submission
        submission.comments.replace_more(limit=None)
        self.comments = submission.comments.list()

    def get_frequency(self):
        """
        (Submission) -> dict: (str, int)

        Returns a dictionary containing the 20 most frequent words
        in a reddit submission ignoring common English words.
        """

        # Update frequency of title
        update(self.frequency, self.title)

        # Remove HTML syntax from body
        soup = bs4.BeautifulSoup(self.body, 'html.parser')
        self.body = soup.get_text()

        # Update frequency of body
        update(self.frequency, self.body)

        # Update frequency of all comments in submission
        for comment in self.comments:
            update(self.frequency, comment.body)

        # Filter common words from frequency dictionary
        self.frequency = filter_common_words(self.frequency)

        # Retrieve the top 20 common words
        self.frequency = get_top_words(self.frequency)

        # Construct dictionary including frequency dictionary and submission attributes
        submission_d = {self.id: {"title": self.title, "num_words": self.total_words,
                                  "subreddit_id": self.subreddit_id, "words": self.frequency,
                                  "last_request": self.last_request
                                  }
                        }

        return submission_d
