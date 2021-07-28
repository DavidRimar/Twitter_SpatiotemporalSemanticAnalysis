from NLPPreProcessor import *
import numpy as np
from config import *
import pandas as pd
import numpy as np
# from models.ModelViews import BristolViewV1
# from models.BristolViewV1 import BristolViewV1
from datetime_truncate import truncate
import time
from DataLoader import *
from models.ModelBristol import *
from sklearn import preprocessing
from sklearn.metrics.pairwise import pairwise_distances
from sklearn import metrics
#import fastcluster
import scipy.cluster.hierarchy as sch
from collections import Counter
from scipy.cluster import hierarchy


class TFIDF():

    def __init__(self, dataframe):

        self.dataframe = dataframe

        self.nlp_pre_processor = NLPPreProcessor(self.dataframe)


    def get_tfidf_stdbscan(self):

        number_of_stdbscan_clusters = 540

        # arrays holding results for all time windows and space
        final_stdbscan_id_list = []
        final_sig_words_dict = []

        # ######## calculate IDF score (using all stdbscan clusters) #######
        raw_tweet_corpus_all = self.nlp_pre_processor.get_raw_tweet_text_array(
            self.dataframe)

        # CLEANSE ALL TWEETS
        cleansed_tweet_corpus_all = self.nlp_pre_processor.cleanse_all_tweets(
            raw_tweet_corpus_all)

        cleansed_tweet_corpus_all_joined = [
            ' '.join(arr) for arr in cleansed_tweet_corpus_all]

        print("Cleansing DONE!")

        # VECTORIZE
        vectorizer = TfidfVectorizer(ngram_range=(1, 1))
        vectorizer.fit_transform(cleansed_tweet_corpus_all_joined)

        # FOR LOOP: iterate through each spatiotemporal cluster
        for stdbscan_id in range(1, number_of_stdbscan_clusters):

            # get the tweets corresponding to the spatiotemporal cluster
            spatiotemp_df = self.dataframe.loc[self.dataframe['stdbscan_02_10800_3'] == stdbscan_id]

            print("length of temp_df\n", len(spatiotemp_df))

            # CLEANSE ALL TWEETS
            raw_tweet_corpus_stdbscan = self.nlp_pre_processor.get_raw_tweet_text_array(
                spatiotemp_df)

            cleansed_tweet_corpus_stdbscan = self.nlp_pre_processor.cleanse_all_tweets(
                raw_tweet_corpus_stdbscan)

            # cleansed_spat_temp_tweet_corpus_joined = [
            #    ' '.join(arr) for arr in cleansed_spat_temp_tweet_corpus]

            # BUILD DOCUMENT
            stdbscan_doc = self.build_document_from_corpus(
                cleansed_tweet_corpus_stdbscan)

            # GET SIGNIFICANT WORDS
            # TF PART: the spat temp document is evaluated in the light
            # of the IDF learned on this temporal window i.e. the IDF part
            stdbscan_response = vectorizer.transform([stdbscan_doc])

            # sorted tfidf
            tfidf_sorted = np.argsort(
                stdbscan_response.toarray()).flatten()[::-1]

            feature_names = vectorizer.get_feature_names()

            feature_array = np.array(vectorizer.get_feature_names())

            tfidf_top_10 = feature_array[tfidf_sorted][:10]
            tfidf_20 = feature_array[tfidf_sorted][10:20]

            # initialize dictionary to hold tfidf results for this d=stdbscan cluster
            sig_weights_current = []
            sig_words_dict_current = {}

            for col in stdbscan_response.nonzero()[1]:
                if feature_names[col] in tfidf_top_10:

                    """
                    word = ""

                    if feature_names[col] == "and":

                        word = tfidf_11

                    else:

                        word = feature_names[col]
                    """
                    word = feature_names[col]

                    weight = stdbscan_response[0, col]

                    print(word, ' - ', weight)

                    # add to weights list
                    sig_weights_current.append(weight)

                    # add to dictionary
                    sig_words_dict_current[word] = weight

            # append this tfidf dict to final list of dicts
            final_sig_words_dict.append(sig_words_dict_current)

            # print("current weights: ", sig_weights_current)
            print("Added sig_words_dict_current:\n ", sig_words_dict_current)

            # APPEND RESULTS TO LISTS (this time window's results)
            final_stdbscan_id_list.append(stdbscan_id)
            final_sig_words_dict.append(sig_words_dict_current)

        # BUILD FINAL DF
        df_tfidf = pd.DataFrame(list(zip(final_stdbscan_id_list, final_sig_words_dict)), columns=[
            "stdbscan_id", "sig_words_dict"])

        print(df_tfidf.head(15))

        # when all time windows are over,
        # we want the df_spat_tfidfs to be concatenated
        # and returned
        return df_tfidf

    def get_tfidf_spat_temp(self):

        number_of_days = 40
        number_of_dbscans = 325  # there is no more than 325

        # arrays holding results for all time windows and space
        final_spat_temp_id_str_list = []
        final_dbscan_id_list = []
        final_temp_ID_list = []
        # final_sig_words_list = []
        # final_sig_weights_list = []
        final_sig_words_dict = []

        # max(df['temp_day_id'])

        # FOR LOOP: slice it by day
        for day in range(1, number_of_days):

            # get df for this time window (across all grids)
            temp_df = self.dataframe.loc[self.dataframe['temp_day_id'] == day]

            print("length of temp_df\n", len(temp_df))

            # ######## calculate IDF score #######
            # raw tweet text array
            raw_tweet_corpus_day = self.nlp_pre_processor.get_raw_tweet_text_array(
                temp_df)

            # CLEANSE ALL TWEETS
            cleansed_tweet_corpus_day = self.nlp_pre_processor.cleanse_all_tweets(
                raw_tweet_corpus_day)

            cleansed_tweet_corpus_day_joined = [
                ' '.join(arr) for arr in cleansed_tweet_corpus_day]

            print("Cleansing DONE!")

            # VECTORIZE
            vectorizer = TfidfVectorizer(ngram_range=(2, 2))
            vectorizer.fit_transform(cleansed_tweet_corpus_day_joined)

            """
            Now, we have the collection of documents with each
            document representing a grid on the same day.
            i.e. the IDF part calculated.
            """

            # arrays holding results for this time window
            # spat_temp_id_str_list = []
            # fishnet_id_list = []
            # temp_ID_list = []
            # sig_words_list = []
            # sig_weights_list = []
            # sig_words_dict = []

            # FOR LOOP: slice by space
            for dbscan in range(0, number_of_dbscans):

                # slice temp_df for this grid
                spat_temp_df = temp_df.loc[temp_df['dbscan_004_5_temp'] == dbscan]

                # if temp day id is not empty
                if (len(spat_temp_df) > 0):

                    print(
                        f"length of spat_temp_df at {day} {dbscan}\n", len(spat_temp_df))

                    # raw tweet text array
                    raw_tweet_corpus_day_grid = self.nlp_pre_processor.get_raw_tweet_text_array(
                        spat_temp_df)

                    # CLEANSE ALL TWEETS
                    cleansed_tweet_corpus_day_grid = self.nlp_pre_processor.cleanse_all_tweets(
                        raw_tweet_corpus_day_grid)

                    # cleansed_spat_temp_tweet_corpus_joined = [
                    #    ' '.join(arr) for arr in cleansed_spat_temp_tweet_corpus]

                    # BUILD DOCUMENT
                    spat_temp_doc = self.build_document_from_corpus(
                        cleansed_tweet_corpus_day_grid)

                    # GET SIGNIFICANT WORDS
                    # TF PART: the spat temp document is evaluated in the light
                    # of the IDF learned on this temporal window i.e. the IDF part
                    day_grid_response = vectorizer.transform([spat_temp_doc])

                    # sorted tfidf
                    tfidf_sorted = np.argsort(
                        day_grid_response.toarray()).flatten()[::-1]

                    feature_names = vectorizer.get_feature_names()

                    feature_array = np.array(vectorizer.get_feature_names())

                    tfidf_top_10 = feature_array[tfidf_sorted][:10]
                    tfidf_11 = feature_array[tfidf_sorted][11]

                    sig_weights_current = []
                    sig_words_dict_current = {}

                    for col in day_grid_response.nonzero()[1]:
                        if feature_names[col] in tfidf_top_10:

                            word = ""

                            if feature_names[col] == "and":

                                word = tfidf_11

                            else:

                                word = feature_names[col]

                            weight = day_grid_response[0, col]

                            print(word, ' - ', weight)

                            # add to weights list
                            sig_weights_current.append(weight)

                            # add to dictionary
                            sig_words_dict_current[word] = weight

                    # append sig weights
                    # sig_weights_list.append(sig_weights_current)

                    final_sig_words_dict.append(sig_words_dict_current)

                    # print("current weights: ", sig_weights_current)
                    # print("current dict: ", sig_words_dict_current)

                    # APPEND RESULTS TO LISTS (this time window's results)
                    spat_temp_id_str_current = str(dbscan) + "_" + str(day)
                    final_spat_temp_id_str_list.append(
                        spat_temp_id_str_current)
                    final_dbscan_id_list.append(dbscan)
                    final_temp_ID_list.append(day)
                    # sig_words_list.append(tfidf_top_10)  # tfidf_top_10 is an array

            # LOOP END: SPATIAL
            # when this time window's spatial loop is over
            # what we have is the data for one day in lists
            # lets append them to the top level lists
            """
            final_spat_temp_id_str_list.append(spat_temp_id_str_list)
            final_fishnet_id_list.append(fishnet_id_list)
            final_temp_ID_list.append(temp_ID_list)
            final_sig_words_list.append(sig_weights_list)
            final_sig_weights_list.append(sig_weights_list)
            final_sig_words_dict.append(sig_words_dict)
            """
        # LOOP END: TEMPORAL

        # BUILD FINAL DF
        df_tfidf = pd.DataFrame(list(zip(final_spat_temp_id_str_list, final_dbscan_id_list, final_temp_ID_list, final_sig_words_dict)), columns=[
            "spat_temp_id_str", "dbscan_004_5_id", "temp_day_id", "sig_words_dict"])

        # when all time windows are over,
        # we want the df_spat_tfidfs to be concatenated
        # and returned
        return df_tfidf

    """
    cleansed_tweet_corpus is an array of arrays where each array contains
    tokens of a single tweet.
    This function joins them all up to form a single document.
    """

    def build_document_from_corpus(self, cleansed_tweet_corpus):

        document_string = ""

        for tweet in cleansed_tweet_corpus:

            for token in tweet:

                document_string += " "

                document_string += token

        return document_string
