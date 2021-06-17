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


def test_time():
    filename = 'STDBSCAN_eubr_bigsea/sample.csv'
    df = pd.read_csv(filename, sep=";", converters={'date_time': parse_dates})
    '''
    First, we transform the lon/lat (geographic coordinates) to x and y
    (in meters), in order to this, we need to select the right epsg (it
    depends on the trace). After that, we run the algorithm.
    '''
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


def main():

    # INSTANTIATE TweetCrawler object
    tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)

    # GET tweets
    query_result_df = tweetCrawler.crawl_data_with_session(
        BristolSet2ST)

    query_result_df = query_result_df.loc[:, [
        'tweet_id', 'created_at', 'final_point_lon', 'final_point_lat']]

    print('QUERY result: ', query_result_df.head())

    start_date = '2021-03-01 00:00:00'
    end_date = '2021-04-08 00:00:00'

    mask = (query_result_df['created_at'] > start_date) & (
        query_result_df['created_at'] <= end_date)

    # query_result_df = query_result_df.loc[mask]

    # SAVE TWEETS TO CSV
    # query_result_df.to_csv('data/bristol_st_all.csv')

    # PARAMETERS
    spatial_threshold = 5000  # meters
    temporal_threshold = 21600  # seconds
    min_neighbors = 5

    # INSTANTIATE
    stdbscan_instance = STDBSCAN(
        spatial_threshold, temporal_threshold, min_neighbors)

    # CONVERT DF TO UTM
    df = convert_to_utm(query_result_df, src_epsg=4326, dst_epsg=27700,
                        col_lat='final_point_lat', col_lon='final_point_lon')

    # CALL fit_transform
    cluster_result = stdbscan_instance.fit_transform(df, col_record_id='tweet_id', col_lat='final_point_lat',
                                                     col_lon='final_point_lat',
                                                     col_time='created_at')

    # SORT BY CREATED AT
    cluster_result.sort_values(by=['created_at'], inplace=True)

    print("cluster_result: ", cluster_result.head())

    # SAVE CLUSTERING RESULT
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    cluster_result.to_csv(
        f'cluster_results/stdbscan_{spatial_threshold}_{temporal_threshold}_{min_neighbors}.csv')

    # READ IN FILE AND LOAD TO DB
    # cluster_results_df = pd.read_csv(
    #    'cluster_results/test.csv', parse_dates=True, index_col=0)

    # print(cluster_results_df.head())

    # print(type(cluster_results_df['tweet_id'][2]))

    # INSTANTIATE DATALOADER
    # dataLoader = DataLoader(DATABASE_URI_TRIAL)

    # dataLoader.inspect(Tweet)

    # pass in the cluster results and update DB
    # dataLoader.update_all(cluster_results_df, Tweet)


def inspect():

    # READ IN FILE AND LOAD TO DB
    cluster_results_df = pd.read_csv(
        'cluster_results/stdbscan_5000_4320_5.csv', parse_dates=True, index_col=0)
    # cluster_results_df = pd.read_csv(
    #    'cluster_results/stdbscan_1500_420_3_20210611-215942.csv', parse_dates=True, index_col=0)

    cluster_results_df.sort_values(by=['created_at'], inplace=True)

    print(cluster_results_df.head())

    print(cluster_results_df['cluster'].value_counts(dropna=False))
    """
    cluster 223 is the largest
    """
    print(cluster_results_df['cluster'].value_counts(normalize=True))

    # SLICE BY CLUSTER ID
    cid_largest = cluster_results_df.loc[cluster_results_df['cluster'] == 1008]

    print(cid_largest.head(10))

    print("min date: ", min(cid_largest['created_at']))
    print("max date: ", max(cid_largest['created_at']))


def load():

    # print("")

    # READ IN FILE AND LOAD TO DB
    cluster_results_df = pd.read_csv(
        'cluster_results/stdbscan_5000_4320_5.csv', parse_dates=True, index_col=0)

    # INSTANTIATE DATALOADER
    dataLoader = DataLoader(DATABASE_URI_RDS_TWEETS)

    # pass in the cluster results and update DB
    dataLoader.update_all(cluster_results_df, BristolSet2ST)


if __name__ == '__main__':
    # df = pd.DataFrame(test_time())
    # print("df head: ", df.head())
    # print("counts:\n", pd.value_counts(df['cluster']))

    # df.to_csv('asd.csv')

    # #####################
    # main()

    inspect()

    # load()
