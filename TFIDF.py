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
from NLPPreProcessor import *
from sklearn import preprocessing
from sklearn.metrics.pairwise import pairwise_distances
from sklearn import metrics
import fastcluster
import scipy.cluster.hierarchy as sch
from collections import Counter
import CMUTweetTagger
from scipy.cluster import hierarchy


class TFIDF():

    def __init__(self, dataframe):

        self.dataframe = dataframe

        self.nlp_pre_processor = NLPPreProcessor(self.dataframe)

    def get_tfidf_spat_temp(self):

        # arrays holding results for all time windows and space
        final_spat_temp_id_str_list = []
        final_fishnet_id_list = []
        final_temp_ID_list = []
        # final_sig_words_list = []
        # final_sig_weights_list = []
        final_sig_words_dict = []

        # max(df['temp_day_id'])

        # FOR LOOP: slice it by day
        for day in range(1, 2):

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
            vectorizer = TfidfVectorizer()
            vectorizer.fit_transform(cleansed_tweet_corpus_day_joined)

            """
            Now, we have the collection of documents
            i.e. the IDF part calculated.
            Next, we build documents per spatial grid
            """

            # arrays holding results for this time window
            # spat_temp_id_str_list = []
            # fishnet_id_list = []
            # temp_ID_list = []
            # sig_words_list = []
            # sig_weights_list = []
            # sig_words_dict = []

            n_of_fishnet_grids = int(max(temp_df['fishnet_c_id']))
            print("fishnet: ", n_of_fishnet_grids)

            # FOR LOOP: slice by space
            for grid in range(1, 4):

                # slice temp_df for this grid
                spat_temp_df = temp_df.loc[temp_df['fishnet_c_id'] == grid]

                print(
                    f"length of spat_temp_df at {day} {grid}\n", len(spat_temp_df))

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
                spat_temp_id_str_current = str(grid) + "_" + str(day)
                final_spat_temp_id_str_list.append(spat_temp_id_str_current)
                final_fishnet_id_list.append(grid)
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
        df_tfidf = pd.DataFrame(list(zip(final_spat_temp_id_str_list, final_fishnet_id_list, final_temp_ID_list, final_sig_words_dict)), columns=[
            "spat_temp_id_str", "fishnet_id", "temp_day_id", "sig_words_dict"])

        # when all time windows are over,
        # we want the df_spat_tfidfs to be concatenated
        # and returned
        return df_tfidf

    def get_tfidf_significant_words(self, fishnet_id):

        spat_temp_id_str_list = []
        fishnet_id_list = []
        temp_ID_list = []
        sig_words_list = []
        sig_weights_list = []
        sig_words_dict = []

        # LOOP THROUGH EACH DAY (i.e. temp_day_ID)
        for i in range(1, 39):

            # df for one time window
            temp_df = self.dataframe.loc[self.dataframe['temp_day_id'] == i]

            print(f"len of temp ID: {i}", len(temp_df))

            # print(temp_df)

            # raw tweet text array
            raw_tweet_corpus = self.nlp_pre_processor.get_raw_tweet_text_array(
                temp_df)

            # CLEANSE ALL TWEETS
            cleansed_tweet_corpus = self.nlp_pre_processor.cleanse_all_tweets(
                raw_tweet_corpus)

            cleansed_tweet_corpus_joined = [
                ' '.join(arr) for arr in cleansed_tweet_corpus]

            # VECTORIZE
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(cleansed_tweet_corpus_joined)

            # BUILD DOCUMENT
            vocab_as_doc = self.build_document_from_corpus(
                cleansed_tweet_corpus)

            # GET SIGNIFICANT WORDS
            #
            response = vectorizer.transform([vocab_as_doc])

            # sorted tfidf
            tfidf_sorted = np.argsort(response.toarray()).flatten()[::-1]

            feature_names = vectorizer.get_feature_names()

            feature_array = np.array(vectorizer.get_feature_names())

            tfidf_top_10 = feature_array[tfidf_sorted][:10]
            tfidf_11 = feature_array[tfidf_sorted][11]

            # print("type of: ", type(top_n))
            # print("type of: ", top_n[0])
            # print("type of: ", top_n[1])
            # print(f"{i}: ", tfidf_top_10)

            sig_weights_current = []
            sig_words_dict_current = {}

            for col in response.nonzero()[1]:
                if feature_names[col] in tfidf_top_10:

                    word = ""

                    if feature_names[col] == "and":

                        word = tfidf_11

                    else:

                        word = feature_names[col]

                    weight = response[0, col]

                    print(word, ' - ', weight)

                    # add to dictionary
                    sig_words_dict_current[word] = weight

                    # add to weights list

                    sig_weights_current.append(weight)

            # BUILD RESULT DF
            spat_temp_id_str_current = str(fishnet_id) + "_" + str(i)
            spat_temp_id_str_list.append(spat_temp_id_str_current)
            fishnet_id_list.append(fishnet_id)
            temp_ID_list.append(i)
            sig_words_list.append(tfidf_top_10)  # tfidf_top_10 is an array

            # append sig weights
            sig_weights_list.append(sig_weights_current)

            sig_words_dict.append(sig_words_dict_current)

            print("current weights: ", sig_weights_current)
            print("current dict: ", sig_words_dict_current)

        # end of loop
        df_tfidf = pd.DataFrame(list(zip(spat_temp_id_str_list, fishnet_id_list, temp_ID_list, sig_words_dict)), columns=[
            "spat_temp_id_str", "fishnet_id", "temp_day_id", "sig_words_dict"])

        # return
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

    def get_clusters_for_all(self):

        # LOOP THROUGH EACH DAY (i.e. temp_day_ID)
        for i in range(1, 39):

            # df for one time window
            temp_df = self.dataframe['temp_day_ID' == i]

    def cluster(self, temp_df, i):

        # raw tweet text array
        raw_tweet_corpus = self.nlp_pre_processor.get_raw_tweet_text_array(
            temp_df)

        # CLEANSE ALL TWEETS
        cleansed_tweet_corpus = self.nlp_pre_processor.cleanse_all_tweets(
            raw_tweet_corpus)

        cleansed_tweet_corpus_joined = [
            ' '.join(arr) for arr in cleansed_tweet_corpus]

        # print(cleansed_tweet_corpus[0:3])
        # print(len(cleansed_tweet_corpus_joined))

        # VECTORIZE
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(cleansed_tweet_corpus_joined)

        # ENSURES ALL VALUES ARE FLOAT
        # Xdense = np.matrix(Xclean).astype('float')
        Xdense = np.matrix(X.toarray()).astype('float')

        # print("X dense: ", Xdense[2])

        # Center to the mean and component wise scale to unit variance.
        X_scaled = preprocessing.scale(Xdense)

        # print("X scaled: ", X_scaled[2])

        # Each sample (i.e. each row of the data matrix) with at least one non zero component is
        # rescaled independently of other samples so that its norm (l1, l2 or inf) equals one.
        X_normalized = preprocessing.normalize(X_scaled, norm='l2')

        # print("X normalized: ", X_normalized[2])

        vocX = vectorizer.get_feature_names()
        # print("Vocabulary (tweets): ", vocX)

        ########
        tweet_unixtime_old = -1
        # fout.write("time window size in mins: " + str(time_window_mins))
        tid_to_raw_tweet = {}
        window_corpus = []
        tid_to_urls_window_corpus = {}
        tids_window_corpus = []
        dfVocTimeWindows = {}
        t = 0
        ntweets = 0
        #################

        ########

        # Hclust: fast hierarchical clustering with fastcluster
        # X is samples by features
        # distMatrix is sample by samples distances

        distMatrix = pairwise_distances(X_normalized, metric='cosine')
        print("Len of DistMatrix: ", len(distMatrix))
        print("Example of DistMatrix: ", distMatrix[2])

        # print("fastcluster, average, cosine")
        # LINKAGE MATRIX ENCODING THE HIERARCHICAL CLUSTERING
        L = fastcluster.linkage(distMatrix, method='average')

        # print("L: ", L)

        dt = 0.7
        print("hclust cut threshold:", dt)
        # indL = sch.fcluster(L, dt, 'distance')
        indL = sch.fcluster(L, dt*distMatrix.max(), 'distance')
        # print("indL:\n", indL)

        # Tweet Cluster Sizes
        freqTwCl = Counter(indL)
        print("n_clusters:", len(freqTwCl))
        # print("freqTWCL:\n", freqTwCl)

        #################
        npindL = np.array(indL)  # unnecessary

        # print("npinL:\n", npindL)

        # VISUALISE DENDOGRAM

        # SAVE CLUSTER RESULTS
        tweet_ids = temp_df['tweet_id']
        tweet_text = temp_df['text']
        cluster_ids = pd.DataFrame(npindL, columns=['cluster'])

        df_concat = pd.concat([tweet_ids, tweet_text, cluster_ids], axis=1)

        print("df_concat: ", df_concat.head(17))

        # EXPORT TO CSV
        df_concat.to_csv(f'cluster_results/fishnet_{i}_tfidf.csv')

        # print("top50 most populated clusters, down to size", max(10, int(X.shape[0]*0.0025)))
        freq_th = max(10, int(X.shape[0]*0.0025))
        print("freq_th\n", freq_th)

        # DENDOGRAM
        # dendogram1 = sch.dendrogram(L, p=35)
        # print("dendo", dendogram)

        # fig, axes = plt.subplots(1, figsize=(8, 3))

        # dendogram2 = hierarchy.dendrogram(
        #    L)

        # plt.show()
