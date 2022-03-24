import re
import string
import numpy as np

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer


def process_article(article):
    """Process article function.
    Input:
        article: a string containing a article
    Output:
        articles_clean: a list of words containing the processed article

    """
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    # tokenize articles
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
    article_tokens = tokenizer.tokenize(article)

    articles_clean = []
    for word in article_tokens:
        if (word not in stopwords_english and  # remove stopwords
                word not in string.punctuation):  # remove punctuation
            # articles_clean.append(word)
            stem_word = stemmer.stem(word)  # stemming word
            articles_clean.append(stem_word)

    return articles_clean


def build_freqs(articles, ys):
    """Build frequencies.
    Input:
        articles: a list of articles
        ys: an m x 1 array with the sentiment label of each article
            (either 0 or 1)
    Output:
        freqs: a dictionary mapping each (word, sentiment) pair to its
        frequency
    """
    # Convert np array to list since zip needs an iterable.
    # The squeeze is necessary or the list ends up with one element.
    # Also note that this is just a NOP if ys is already a list.
    yslist = np.squeeze(ys).tolist()

    # Start with an empty dictionary and populate it by looping over all articles
    # and over all processed words in each article.
    freqs = {}
    for y, article in zip(yslist, articles):
        for word in process_article(article):
            pair = (word, y)
            if pair in freqs:
                freqs[pair] += 1
            else:
                freqs[pair] = 1

    return freqs