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

    def get_tfidf_significant_words(self):

        fishnet_id_list = []
        temp_ID_list = []
        sig_words_list = []

        # LOOP THROUGH EACH DAY (i.e. temp_day_ID)
        for i in range(1, 3):

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
            response = vectorizer.transform([vocab_as_doc])
            feature_names = vectorizer.get_feature_names()

            # for col in response.nonzero()[1]:
            # if response[0, col] > 0.4:
            #    print(feature_names[col], ' - ', response[0, col])

            # construct line to write
            # line = "8," + str(i) + "," + feature_names

            feature_array = np.array(vectorizer.get_feature_names())
            tfidf_sorting = np.argsort(response.toarray()).flatten()[::-1]

            print("asfa \n", tfidf_sorting)

            n = 10
            top_n = feature_array[tfidf_sorting][:n]

            print("type of: ", type(top_n))
            print("type of: ", top_n[0])
            print("type of: ", top_n[1])

            print(f"{i}: ", top_n)

            # BUILD RESULT DF
            fishnet_id_list.append(2)
            temp_ID_list.append(i)
            sig_words_list.append(top_n)

        # end of loop
        df_tfidf = pd.DataFrame(list(zip(fishnet_id_list, temp_ID_list, sig_words_list)), columns=[
                                "fishnet_id", "temp_day_id", "sig_words_array"])

        # return
        return df_tfidf

    """
    cleansed_tweet_corpus is an array of arrays where each array contains
    tokens of a single tweet.
    The aim is to join them up as a single document, to get a list of significant words.
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
        #Xdense = np.matrix(Xclean).astype('float')
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
        #dendogram1 = sch.dendrogram(L, p=35)
        # print("dendo", dendogram)

        #fig, axes = plt.subplots(1, figsize=(8, 3))

        # dendogram2 = hierarchy.dendrogram(
        #    L)

        # plt.show()
