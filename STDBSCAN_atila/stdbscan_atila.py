import math
from datetime import timedelta
from geopy.distance import great_circle

"""
source: https://github.com/gitAtila/ST-DBSCAN
"""

"""
INPUTS:
    df={o1,o2,...,on} Set of objects
    spatial_threshold = Maximum geographical coordinate (spatial) distance value
    temporal_threshold = Maximum non-spatial distance value
    min_neighbors = Minimun number of points within Eps1 and Eps2 distance
OUTPUT:
    C = {c1,c2,...,ck} Set of clusters
"""


def ST_DBSCAN(df, spatial_threshold, temporal_threshold, min_neighbors):
    cluster_label = 0
    NOISE = -1
    UNMARKED = 777777
    stack = []

    # initialize each point with unmarked
    df['cluster'] = UNMARKED

    # for each point in datframe
    for index, point in df.iterrows():

        # if UNMARKED
        if df.loc[index]['cluster'] == UNMARKED:

            # RETRIEVE NEIGHBORS (returns a collection of tweets)
            neighborhood = retrieve_neighbors(
                index, df, spatial_threshold, temporal_threshold)

            # IF: THE TWEET IS NOISE
            if len(neighborhood) < min_neighbors:
                df.at[index, 'cluster'] = NOISE

            # ELSE: THE TWEET IS A CORE POINT
            else:

                # assign cluster ID to the core point
                cluster_label = cluster_label + 1

                df.at[index, 'cluster'] = cluster_label

                # for each tweet in the neighborhood
                for neig_index in neighborhood:

                    # assign core's label
                    df.at[neig_index, 'cluster'] = cluster_label

                    # append neighborhood to stack
                    stack.append(neig_index)

                # EXPAND THE INITIAL CLUSTER BY looking at each neighbor point
                # within stack, and decide if it is "CORE" or a "BORDER" point
                # do this as long as the the stack has any potential core points
                while len(stack) > 0:

                    current_point_index = stack.pop()

                    # find new neighbor points from current point
                    new_neighborhood = retrieve_neighbors(
                        current_point_index, df, spatial_threshold, temporal_threshold)

                    # IF CURRENT POINT IS A CORE
                    if len(new_neighborhood) >= min_neighbors:

                        # FOR EACH NEW NEIGHBOR POINT
                        for neig_index in new_neighborhood:

                            neig_cluster = df.loc[neig_index]['cluster']

                            if (neig_cluster != NOISE) & (neig_cluster == UNMARKED):

                                # TODO: verify cluster average before add new point

                                # ASSIGN CLUSTER ID to this point
                                df.at[neig_index, 'cluster'] = cluster_label

                                # ADD TO THE STACK SO that this point is looked at again
                                # and assessed if it is a core or border point
                                stack.append(neig_index)

    return df


def retrieve_neighbors(index_center, df, spatial_threshold, temporal_threshold):

    # CONSIDER THIS TWEET AS THE CORE POINT
    center_point = df.loc[index_center]

    # A SET OF TWEETS TO RETURN IF THIS TWEET IS A CORE POINT
    # othwerwise, empty
    neigborhood = []

    # FILTER BY TIME
    """
    Since the time window depends on the current point's creation time,
    and each neighbor point is evaluated sequentially, the final time
    window for a particular cluster can be of any length.
    In other words, the time window of a cluster, similarly to the spatial
    boundary, is arbitrarily determined by the algorithm.
    The minutes parameter is only used as a boundary for that particular point,
    additional neighbor points will therefore have a new time boundary and so on.
    """
    min_time = center_point['date_time'] - \
        timedelta(minutes=temporal_threshold)
    max_time = center_point['date_time'] + \
        timedelta(minutes=temporal_threshold)
    df = df[(df['date_time'] >= min_time) & (df['date_time'] <= max_time)]

    # filter by distance
    for index, point in df.iterrows():
        if index != index_center:
            distance = great_circle((center_point['latitude'], center_point['longitude']), (
                point['latitude'], point['longitude'])).meters
            if distance <= spatial_threshold:
                neigborhood.append(index)

    return neigborhood
