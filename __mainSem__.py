from TweetCrawler import *
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


def main():

    # INSTANTIATE TweetCrawler object
    tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)

    # GET tweets
    query_df = tweetCrawler.crawl_data_with_session(
        BristolSet2FishNet, 8)

    # save it to csv
    # query_df.to_csv('data/bristol_sem.csv', sep=",")

    # CONVERT 'created_at' to daily
    # bristol_df = pd.read_csv('data/bristol_sem.csv',
    #                         parse_dates=True, index_col=0)

    # print(type(data["created_at"][1]))

    # convert "created_at" to datetime
    # bristol_df["created_at"] = pd.to_datetime(bristol_df["created_at"])
    query_df["created_at"] = pd.to_datetime(query_df["created_at"])

    # sort by created_at
    # bristol_df = bristol_df.sort_values(by="created_at")
    query_df = query_df.sort_values(by="created_at")

    # print(type(data["created_at"][1]))

    print("Shape of query df: ", query_df.shape)

    # DATA PREPROCESSOR
    data_pre_processor = NLPPreProcessor(query_df)

    # GET WORD FREQ DATAFRAME PER DAY (for top N words)
    raw_tweet_corpus = data_pre_processor.get_raw_tweet_text_array(query_df)

    # print("c: ", raw_tweet_corpus[0])
    # print("lenght of c: ", len(raw_tweet_corpus))

    # take a subset of the raw tweet corpus
    #sample = raw_tweet_corpus[0:15]

    # print(len(sample))

    # cleanse all tweets
    cleansed_tweet_corpus = data_pre_processor.cleanse_all_tweets(
        raw_tweet_corpus)

    cleansed_tweet_corpus_joined = [
        ' '.join(arr) for arr in cleansed_tweet_corpus]

    # print(cleansed_tweet_corpus[0:3])
    print(len(cleansed_tweet_corpus_joined))

    # VECTORIZE
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(cleansed_tweet_corpus_joined)

    # print("vocab length: ", len(vectorizer.get_feature_names()))

    print("X SHAPE: ", X[2].toarray())

    #  //// REMOVE TWEETS OF SMALLER THAN SIZE 4
    map_index_after_cleaning = {}

    Xclean = np.zeros((1, X.shape[1]))

    for i in range(0, X.shape[0]):
        # keep sample with size at least 5
        # (X[i] is accessing rows)
        if X[i].sum() > 0.4:
            Xclean = np.vstack([Xclean, X[i].toarray()])
            # print("CLEAN:\n", Xclean.shape)
            # print("MAP INDEX:\n", map_index_after_cleaning)
            map_index_after_cleaning[Xclean.shape[0] - 2] = i

        else:
            # show what is removed
            print("X SMALL: ", X[i].toarray())

    Xclean = Xclean[1:, ]  # remove first row with zeros

    print("X SHAPE: ", Xclean.shape)

    # ENSURES ALL VALUES ARE FLOAT
    Xdense = np.matrix(Xclean).astype('float')

    # print("X dense: ", Xdense[2])

    # Center to the mean and component wise scale to unit variance.
    X_scaled = preprocessing.scale(Xdense)

    # print("X scaled: ", X_scaled[2])

    # Each sample (i.e. each row of the data matrix) with at least one non zero component is
    # rescaled independently of other samples so that its norm (l1, l2 or inf) equals one.
    X_normalized = preprocessing.normalize(X_scaled, norm='l2')

    # print("X normalized: ", X_normalized[2])

    vocX = vectorizer.get_feature_names()
    print("Vocabulary (tweets): ", vocX)

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
    tweet_ids = query_df['tweet_id']
    tweet_text = query_df['text']
    cluster_ids = pd.DataFrame(npindL, columns=['cluster'])

    df_concat = pd.concat([tweet_ids, tweet_text, cluster_ids], axis=1)

    print("df_concat: ", df_concat.head(17))

    # EXPORT TO CSV
    df_concat.to_csv('cluster_results/fishnet_8_tfidf_all.csv')

    # print("top50 most populated clusters, down to size", max(10, int(X.shape[0]*0.0025)))
    freq_th = max(10, int(X.shape[0]*0.0025))
    print("freq_th\n", freq_th)

    # DENDOGRAM
    dendogram1 = sch.dendrogram(L, p=35)
    # print("dendo", dendogram)

    fig, axes = plt.subplots(1, figsize=(8, 3))

    dendogram2 = hierarchy.dendrogram(
        L)

    plt.show()

    # TWEET TAGGER
    """
    dfX = X.sum(axis=0)
    # print "dfX:", dfX
    dfVoc = {}
    wdfVoc = {}
    boosted_wdfVoc = {}
    keys = vocX
    vals = dfX
    boost_entity = {}
    pos_tokens = CMUTweetTagger.runtagger_parse(
        [term.upper() for term in vocX])
    # print "detect entities", pos_tokens
    for l in pos_tokens:
        term = ''
        for gr in range(0, len(l)):
            term += l[gr][0].lower() + " "
        if "^" in str(l):
            boost_entity[term.strip()] = 2.5
        else:
            boost_entity[term.strip()] = 1.0

    for k, v in zip(keys, vals):
        dfVoc[k] = v

    for k in dfVoc:
        try:
            dfVocTimeWindows[k] += dfVoc[k]
            avgdfVoc = (dfVocTimeWindows[k] - dfVoc[k])/(t - 1)
            # avgdfVoc = (dfVocTimeWindows[k] - dfVoc[k])
        except:
            dfVocTimeWindows[k] = dfVoc[k]
            avgdfVoc = 0
        wdfVoc[k] = (dfVoc[k] + 1) / (np.log(avgdfVoc + 1) + 1)
        try:
            boosted_wdfVoc[k] = wdfVoc[k] * boost_entity[k]
        except:
            boosted_wdfVoc[k] = wdfVoc[k]
    """

    # CLUSTER SCOING AND ANALYSIS
    """
    cluster_score = {}

    for clfreq in freqTwCl.most_common(50):
        cl = clfreq[0]
        freq = clfreq[1]
        cluster_score[cl] = 0
        if freq >= freq_th:
            # print "\n(cluster, freq):", clfreq
            clidx = (npindL == cl).nonzero()[0].tolist()
            cluster_centroid = X[clidx].sum(axis=0)
            # print "centroid_array:", cluster_centroid
            try:
                # orig_tweet = window_corpus[map_index_after_cleaning[i]].decode("utf-8")
                cluster_tweet = vectorizer.inverse_transform(
                    cluster_centroid)
                # print orig_tweet, cluster_tweet, urls_window_corpus[map_index_after_cleaning[i]]
                # print orig_tweet
                # print "centroid_tweet:", cluster_tweet
                for term in np.nditer(cluster_tweet):
                    # print "term:", term#, wdfVoc[term]
                    try:
                        cluster_score[cl] = max(
                            cluster_score[cl], boosted_wdfVoc[str(term).strip()])
                        # cluster_score[cl] += wdfVoc[str(term).strip()] * boost_entity[str(term)] #* boost_term_in_article[str(term)]
                        # cluster_score[cl] = max(cluster_score[cl], wdfVoc[str(term).strip()] * boost_term_in_article[str(term)])
                        # cluster_score[cl] = max(cluster_score[cl], wdfVoc[str(term).strip()] * boost_entity[str(term)])
                        # cluster_score[cl] = max(cluster_score[cl], wdfVoc[str(term).strip()] * boost_entity[str(term)] * boost_term_in_article[str(term)])
                    except:
                        pass
            except:
                pass
            cluster_score[cl] /= freq
        else:
            break

    sorted_clusters = sorted(
        ((v, k) for k, v in cluster_score.items()), reverse=True)

    print("sorted cluster_score:", sorted_clusters)
    """


if __name__ == "__main__":

    main()
