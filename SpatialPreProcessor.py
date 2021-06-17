import pandas as pd


class SpatialPreProcessor():

    ### CONSTRUCTOR ###
    def __init__(self, dataframe):

        self.originial_dataframe = dataframe

    def get_df_for_stdbscan_atila(self):

        tweet_id_list = []
        longitude_list = []
        latitude_list = []
        timestamp_list = []

        # for each row in dataframe
        for index, row in self.originial_dataframe.iterrows():

            """
            # if no geo coordinates are used
            if row['geo_coordinates_coords'] == None:

                # DONT USE for now
                print("None")

            else:
            """
            tweet_id_list.append(row['tweet_id'])

            longitude_list.append(row['final_point_lon'])

            latitude_list.append(row['final_point_lat'])

            timestamp_list.append(row['created_at'])

        converted_df = pd.DataFrame(
            list(zip(tweet_id_list, latitude_list, longitude_list, timestamp_list)), columns=['tweet_id', 'latitude', 'longitude', 'date_time'])

        return converted_df
