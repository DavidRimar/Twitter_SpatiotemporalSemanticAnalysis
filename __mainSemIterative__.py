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
from models.ModelFishNet import *
from models.ModelDBSCAN import *
from NLPPreProcessor import *
from sklearn import preprocessing
from sklearn.metrics.pairwise import pairwise_distances
from sklearn import metrics
import fastcluster
import scipy.cluster.hierarchy as sch
from collections import Counter
from scipy.cluster import hierarchy
from TFIDF import *
from dataloaders.FishNetLoader import *
from dataloaders.DBSCANloader import *


def main():

    # INSTANTIATE TweetCrawler object
    tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)

    # GET tweets
    query_df = tweetCrawler.crawl_data_with_session(
        Bristol_Set2_DBSCAN)

    # convert "created_at" to datetime
    query_df["created_at"] = pd.to_datetime(query_df["created_at"])

    # sort by created_at
    # bristol_df = bristol_df.sort_values(by="created_at")
    # query_df = query_df.sort_values(by="created_at")

    # INSTANTIATE TFIDF
    tfidf = TFIDF(query_df)

    # sig_words_df = tfidf.get_tfidf_significant_words(fishnet_id)
    sig_words_df = tfidf.get_tfidf_spat_temp()

    print("sig_words:\n", sig_words_df)

    # LOAD DATA
    data_loader = DataLoader(DATABASE_URI_RDS_TWEETS)

    data_loader.update_all(sig_words_df, BristolDBSCAN_004_5)

    # sig_words_df.to_csv("fishnet_results/sig_words/bristol_trial_2opp.csv")

    #print(sig_words_df.loc[:, "sig_words_array"])
    #print(sig_words_df.loc[:, "sig_weights_array"])
    #print(sig_words_df.loc[:, "sig_words_dict"])


def load_fishnet_table():

    df = pd.read_csv('fishnet_table_80_443.csv')

    print(df.head(10))

    fishnet_loader = FishNetLoader(DATABASE_URI_RDS_TWEETS)

    fishnet_loader.transform_and_load(df)


def load_dbscan_table():

    df = pd.read_csv('DBSCAN_table2.csv')

    print(df.head(10))

    dbscan_loader = DBSCANLoader(DATABASE_URI_RDS_TWEETS)

    dbscan_loader.transform_and_load(df)


if __name__ == "__main__":

    main()

    # load_fishnet_table()

    # load_dbscan_table()
