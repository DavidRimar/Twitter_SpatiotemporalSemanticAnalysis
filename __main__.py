from TweetCrawler import *
from config import *
import pandas as pd
# from models.ModelViews import BristolViewV1
# from models.BristolViewV1 import BristolViewV1
# from models.ModelLocal import *
from models.ModelBristol import *
from datetime_truncate import truncate
from STDBSCAN_atila.stdbscan_atila import *
from SpatialPreProcessor import *
import time
from DataLoader import *


def main():

    # INSTANTIATE TweetCrawler object
    tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)

    # GET tweets
    query_result_df = tweetCrawler.crawl_data_with_session(
        BristolST)

    print('QUERY: ', query_result_df.head())

    # INSPECT
    # print(type(results_textual_generic.iloc[1]['created_at']))
    # print(results_textual_generic['created_at'].head())
    # print(results_textual_generic.columns)

    # CONVERT 'created_at' to daily
    # results_textual_generic['created_at'] = results_textual_generic['created_at'].dt.floor(
    #    'd')

    # df_table must have the columns: 'latitude', 'longitude' and 'date_time'
    spatial_pre_processor = SpatialPreProcessor(query_result_df)

    df_table = spatial_pre_processor.get_df_for_stdbscan_atila()
    print("df_table: ", df_table.head())

    spatial_threshold = 1000  # meters
    temporal_threshold = 300  # minutes
    min_neighbors = 3

    df_clustering = ST_DBSCAN(
        df_table, spatial_threshold, temporal_threshold, min_neighbors)
    print("df_clustering head: ", df_clustering.head())

    # SAVE CLUSTERING RESULT
    timestr = time.strftime("%Y%m%d-%H%M%S")
    df_clustering.to_csv(
        f'cluster_results/stdbscan_{spatial_threshold}_{temporal_threshold}_{min_neighbors}_{timestr}.csv')

    # READ IN FILE AND LOAD TO DB
    # cluster_results_df = pd.read_csv(
    #    'cluster_results/test.csv', parse_dates=True, index_col=0)

    # print(cluster_results_df.head())

    # print(type(cluster_results_df['tweet_id'][2]))

    # INSTANTIATE DATALOADER
    #dataLoader = DataLoader(DATABASE_URI_TRIAL)

    # dataLoader.inspect(Tweet)

    # pass in the cluster results and update DB
    #dataLoader.update_all(cluster_results_df, Tweet)


if __name__ == "__main__":

    main()
