# Name: submission.py
# Author: Robin Goyal
# Last-Modified: March 13, 2018
# Purpose: Class representing a reddit submission


import praw
from datetime import datetime
import bs4
import re
from nltk.corpus import stopwords


def update_dict(words_freq, string):
    """
    (dict: (str, int), str))

    Update dict from the frequency of words in string.

    Example:
    >>> dict = {"the": 2, "bird": 3}
    >>> update_freq_dict(dict, "the bird is red")
    >>> dict
    {"the": 3, "bird": 4, "is": 1, "red": 1}
    """

    parsed_words = parse_string(string)

    # Lowercase word for consistency
    for word in parsed_words:
        word = word.lower()
        words_freq[word] = words_freq.get(word, 0) + 1


def parse_string(string):
    """
    (str) -> list: str

    Returns a list of lowercase words from string after
    parsing punctuation and whitespace.

    Example:
    >>> parse_string("It's the first day of the\n New Year")
    ["its", "the", "first", "day", "of", "the", "new", "year"]
    """

    regex = r'[^\w\s]|_'
    parsed_words = re.sub(regex, '', string).split()

    return parsed_words


def filter_common_words(words_freq):
    """
    (dict: (str, int)) -> (dict: (str, int))

    Returns a dictionary with common english words filtered
    from dict as specified by nltk.corpus.stopwords.words.

    Example:
    >>> filter_common_words({"blue": 3, "the": 2, "sky": 3, "is": 1})
    {"blue": 3, "sky": 3}
    """

    d = words_freq.copy()

    common_words = parse_string(" ".join(stopwords.words('english')))

    filtered_word_freq = {word: d[word] for word in d if word not in common_words}

    return filtered_word_freq


def get_top_words(words_freq):
    """
    (dict: (str, int)) -> (dict: (str, int))

    Returns a dictionary containing the 15 most frequent
    words from dict and the remaining word frequencies
    summed as a single key known as "others". Original
    dictionary is returned if less than 15 words.
    """

    d = {}

    sorted_words_freq = sorted(words_freq, key=words_freq.get, reverse=True)
    for k in sorted_words_freq[:20]:
        d[k] = words_freq[k]

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

        # Retrieve all comments from submission
        submission.comments.replace_more(limit=None)
        self.comments = submission.comments.list()

    def get_freq_dict(self):
        """
        (Submission) -> dict: (str, int)

        Returns a dictionary containing the 20 most frequent words
        in a reddit submission ignoring common English words.
        """

        # Update frequency of title
        update_dict(self.frequency, self.title)

        # Remove HTML syntax from body
        soup = bs4.BeautifulSoup(self.body, 'html.parser')
        self.body = soup.get_text()

        # Update frequency of body
        update_dict(self.frequency, self.body)

        # Update frequency of all comments in submission
        for comment in self.comments:
            update_dict(self.frequency, comment.body)

        # Filter common words from frequency dictionary
        self.frequency = filter_common_words(self.frequency)

        # Retrieve the top 20 common words
        self.frequency = get_top_words(self.frequency)

        return self.frequency
