#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TweetCrawler import *
from config import *
from datetime import datetime
import time
import pandas as pd
import numpy as np
from STDBSCAN_eubr_bigsea.stdbscan import STDBSCAN
from STDBSCAN_eubr_bigsea.coordinates import convert_to_utm
from DataLoader import *
from models.ModelBristol import *


"""
SOURCE: https://github.com/eubr-bigsea/py-st-dbscan
"""


def parse_dates(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')


def plot_clusters(df, output_name):
    import matplotlib.pyplot as plt

    labels = df['cluster'].values
    X = df[['longitude', 'latitude']].values

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('ST-DSCAN: #n of clusters {}'.format(len(unique_labels)))
    plt.show()
    # plt.savefig(output_name)

def load():

    # READ IN FILE AND LOAD TO DB
    cluster_results_df = pd.read_csv(
        'cluster_results/stdbscan_0.1_10800_3.csv', parse_dates=True, index_col=0)

    # INSTANTIATE DATALOADER
    dataLoader = DataLoader(DATABASE_URI_RDS_TWEETS)

    # pass in the cluster results and update DB
    dataLoader.update_all(cluster_results_df, Bristol_Set2_TextClassifier_70)


def test_time():
    
    filename = 'STDBSCAN_eubr_bigsea/sample.csv'
    
    df = pd.read_csv(filename, sep=";", converters={'date_time': parse_dates})
    
    # INIT ST_DBSCAN
    st_dbscan = STDBSCAN(spatial_threshold=500, temporal_threshold=600,
                         min_neighbors=5)

    # CONVERT DF TO UTM
    df = convert_to_utm(df, src_epsg=4326, dst_epsg=32633,
                        col_lat='latitude', col_lon='longitude')

    # CALL fit_transform
    result_t600 = st_dbscan.fit_transform(df, col_record_id='ID_RECORD', col_lat='latitude',
                                          col_lon='longitude',
                                          col_time='date_time')

    print("result_t600: ", result_t600.head())

    return result_t600

def inspect(df):
    
    df.sort_values(by=['created_at'], inplace=True)

    print(df.head())

    print("VALUE COUNTS:\n", df['cluster'].value_counts(
        dropna=False).head(30))

    # cluster_results_df['cluster'].value_counts(
    #    dropna=False).to_csv("valuecounts.csv")
    """
    cluster 223 is the largest
    """

    print(df['cluster'].value_counts(normalize=True))

    # SLICE BY CLUSTER ID
    cid_largest = df.loc[df['cluster'] == 223]

    print(cid_largest.head(10))

    # INSPECT SPATIAL AND TEMPORAL EXTENT of the largest cluster
    print("min date: ", min(cid_largest['created_at']))
    print("max date: ", max(cid_largest['created_at']))

    print("min lon: ", min(cid_largest['final_point_lon']))
    print("max lon: ", max(cid_largest['final_point_lon']))

    print("min lat: ", min(cid_largest['final_point_lat']))
    print("max lat: ", max(cid_largest['final_point_lat']))


"""
1. Queries tweets
2. Inspects clusters spatially and temporally (Optional - before loading)
3. Loads to DB
"""    
def main():

    # INSTANTIATE TweetCrawler object
    tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)

    # GET tweets
    query_result_df = tweetCrawler.crawl_data_with_session(
        Bristol_Set2_TextClassifier_70)

    # PARAMETERS
    spatial_threshold = 0.3  # meters
    # seconds (3600 = 1 HOUR, 10800 = 3 HOURS, 21600 = 6 HOURS)
    temporal_threshold = 10800
    min_neighbors = 3

    # INSTANTIATE STDBSCAN
    stdbscan_instance = STDBSCAN(
        spatial_threshold, temporal_threshold, min_neighbors)

    # CALL fit_transform
    cluster_result = stdbscan_instance.fit_transform(df, col_record_id='tweet_id', col_lat='final_point_lat',
                                                     col_lon='final_point_lon',
                                                     col_time='created_at')

    # SAVE CLUSTERING RESULT
    #cluster_result.to_csv(
    #    f'cluster_results/stdbscan_{spatial_threshold}_{temporal_threshold}_{min_neighbors}.csv')

    # INSPECT
    # inspect(cluster_result)

    # PLOT
    # plot_clusters(cluster_result,
                    f"{temporal_threshold}_{spatial_threshold}_{min_neighbors}.jpg")

    # LOAD
    load(cluster_result)


if __name__ == '__main__':
    
    # call main
    main()