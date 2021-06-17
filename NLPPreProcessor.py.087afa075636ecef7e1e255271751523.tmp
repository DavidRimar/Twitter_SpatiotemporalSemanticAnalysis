from string import punctuation
from nltk.tokenize import TweetTokenizer
import inflect
import html
from numpy.compat import unicode
import contractions
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import collections
import nltk
from nltk.corpus import stopwords
import unicodedata
import re
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer

# STEP 1: BUILD CORPUS

# STEP 2: VECTORIZE CORPUS

# STEP 3: TRANFORM TO X

# STEP 3: SCALE AND NORMALIZE X ???

# STEP 5: DISTMATRIX ???

# STEP 6: FASTCLUSTER
# =====================

# process_json_tweet()

# includes preprocessing and tokenization

# returns an array of tokens


"""
sources:
1. https://gist.github.com/MrEliptik/b3f16179aa2f530781ef8ca9a16499af

2. https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/calculate-tweet-word-frequencies-in-python/

"""

"""
Crawls tweets from database.
Carries out NLP data pre-processing tasks on the text.
Yields top N most frequent words per day.
Creates a excel file with the frequency counts for each word and day.
"""


class NLPPreProcessor():

    ### CONSTRUCTOR ###
    def __init__(self, sql_result_as_df):

        ### INSTANCE VARIABLES ###
        self.original_df = sql_result_as_df

        # self.unique_dates = self.get_unique_dates(sql_result_as_df)

        self.raw_tweet_text_array = self.get_raw_tweet_text_array(
            sql_result_as_df)

        self.cleansed_tweet_text_array = []

    # ///// CONVERSIONS ////////

    # converts the text column of the DataFrame to array
    def get_raw_tweet_text_array(self, dataframe):

        return dataframe.loc[:, 'text'].values

    # ///// CONVERSIONS END ////////

    # ///// PREPROCESSING FUNCTIONS ////////

    def remove_urls(self, tweet_text):
        """Replace URLs found in a text string with nothing
        (i.e. it will remove the URL from the string).

        Parameters
        ----------
        txt : string
            A text string that you want to parse and remove urls.

        Returns
        -------
        The same txt string with url's removed.
        """

        url_free_tweet_text = " ".join(
            re.sub(r"http\S+", "", tweet_text).split())

        return url_free_tweet_text

    def fix_contractions(self, tweet_text):

        return contractions.fix(tweet_text)

    def unescape_html_entities(self, text):
        """Converts HTML entities to unicode."""
        text = html.unescape(text)
        return text

    def remove_non_ascii_characters(self, tweet_tokens):

        new_tokens = []

        for token in tweet_tokens:

            new_token = unicodedata.normalize('NFKD', token).encode(
                'ascii', 'ignore').decode('utf-8', 'ignore')

            new_tokens.append(new_token)

        return new_tokens

    def convert_to_lowercase(self, tokenized_tweet):

        tokenized_tweet_lc = []

        for word in tokenized_tweet:

            tokenized_tweet_lc.append(word.lower())

        return tokenized_tweet_lc

    def remove_punctuation(self, tweet_tokens):

        # use Python's string punctuation except # and @
        my_punctuation = punctuation.replace("@", "")
        my_punctuation = my_punctuation.replace("#", "")

        my_punc_list = []

        for s in my_punctuation:
            my_punc_list.append(s)

        new_tokens = []
        for token in tweet_tokens:
            # new_token = re.sub(r'[^\w\s]', '', token)
            new_token = token

            for punc in my_punc_list:

                new_token = new_token.replace(punc, '')

            # @ not used to indicate username but the word at
            if new_token != '' and new_token != '@':
                new_tokens.append(new_token)

        return new_tokens

    def replace_numbers_with_words(self, tweet_tokens):

        p = inflect.engine()

        new_tokens = []
        for token in tweet_tokens:
            if token.isdigit():
                new_token = p.number_to_words(token)
                new_tokens.append(new_token)
            else:
                new_tokens.append(token)
        return new_tokens

    # words is an array

    def remove_stopwords(self, single_tweet_tokenized):

        new_single_tweet = []

        for word in single_tweet_tokenized:

            if word not in stopwords.words('english'):

                new_single_tweet.append(word)

        return new_single_tweet

    def cleanse_single_tweet(self, single_tweet):

        # REMOVE URL
        single_tweet = self.remove_urls(single_tweet)

        # REMOVE CONTRACTIONs
        single_tweet = self.fix_contractions(single_tweet)

        # UNESCAPE HTML ENTITIES
        single_tweet = self.unescape_html_entities(single_tweet)

        # TOKENIZE WORDS
        tweet_tokenizer = TweetTokenizer()
        tokenized_tweet = tweet_tokenizer.tokenize(single_tweet)

        # tokenized_tweet = nltk.word_tokenize(single_tweet)

        # REMOVE NON-ASCII
        clean_tokenized_tweet = self.remove_non_ascii_characters(
            tokenized_tweet)

        # CONVERT TO LOWERCASE
        clean_tokenized_tweet = self.convert_to_lowercase(
            clean_tokenized_tweet)

        # REMOVE PUNCTUATION
        clean_tokenized_tweet = self.remove_punctuation(clean_tokenized_tweet)

        # REPLACE NUMBERS
        clean_tokenized_tweet = self.replace_numbers_with_words(
            clean_tokenized_tweet)

        # REMOVE STOP WORDS
        clean_tokenized_tweet = self.remove_stopwords(clean_tokenized_tweet)

        return clean_tokenized_tweet

    def cleanse_all_tweets(self, tweet_array_to_cleanse):

        cleansed_tweets_array = []

        for tweet in tweet_array_to_cleanse:

            # print("RAW TWEET:\n", tweet)

            # cleansed version of the tweet
            cleansed_single_tweet = self.cleanse_single_tweet(tweet)

            # print("CLEANSED TWEET:\n", cleansed_single_tweet)

            # append to cleansed tweets array
            cleansed_tweets_array.append(cleansed_single_tweet)

        # self.cleansed_tweet_text_array = cleansed_tweets_array

        return cleansed_tweets_array

    # ///// PREPROCESSING FUNCTIONS END ////////

    # INSPECT CLEANSED TWEETS

    def inspect(self):

        print("RAW: ", self.raw_tweet_text_array[2])
        print("CLEANSED", self.cleansed_tweet_text_array[2])

        print("RAW: ", self.raw_tweet_text_array[3])
        print("CLEANSED", self.cleansed_tweet_text_array[3])

        print("RAW: ", self.raw_tweet_text_array[21])
        print("CLEANSED", self.cleansed_tweet_text_array[21])

    # BUILD_WORD_CORPUS

    def build_word_corpus(self, cleansed_tweets_array):
        """
        Returns an array of unique words from an array of documents.
        """
        flattened_word_corpus = [
            item for sublist in cleansed_tweets_array for item in sublist]

        return flattened_word_corpus

    def build_corpus(self):
        print("")

        corpus = ['This is the first document.',
                  'This document is the second document.']

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(corpus)

        print(vectorizer.get_feature_names())
