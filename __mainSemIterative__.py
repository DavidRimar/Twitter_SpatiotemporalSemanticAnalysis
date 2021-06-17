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
from TFIDF import *
from FishNetLoader import *


def main():

    # INSTANTIATE TweetCrawler object
    tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)

    # GET tweets
    query_df = tweetCrawler.crawl_data_with_session(
        BristolFishNet_11_5, 2)

    # convert "created_at" to datetime
    query_df["created_at"] = pd.to_datetime(query_df["created_at"])

    # sort by created_at
    # bristol_df = bristol_df.sort_values(by="created_at")
    query_df = query_df.sort_values(by="created_at")

    tfidf = TFIDF(query_df)

    sig_words_df = tfidf.get_tfidf_significant_words()

    sig_words_df.to_csv("fishnet_results/sig_words/test.csv")


def load_fishnet_table():

    df = pd.read_csv('fishnet_table.csv')

    print(df.head(10))

    fishnet_loader = FishNetLoader(DATABASE_URI_RDS_TWEETS)

    fishnet_loader.transform_and_load(df)


if __name__ == "__main__":

    # main()

    load_fishnet_table()
