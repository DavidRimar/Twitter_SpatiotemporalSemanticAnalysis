from config import *
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import json
from sqlalchemy import update
import math

"""
The TweetLoader class takes care of transforming the fields from a response
to adhere to the data schema represented by the Tweet class.
It uses sqlAlchemy to load the tweets to a DB.
"""


class DataLoader():

    # CONSTRUCTOR
    def __init__(self, database_url):

        # INSTANCE VARIABLES

        # an engine to communicate with PostgreSQL
        self.engine = create_engine(database_url)

        # a Session object to manage connections (session starts)
        self.Session = sessionmaker(bind=self.engine)

    ### METHODS ###

    # START LOAD
    """
    WE WANT TO UPDATE COLUMN VALUES BASED
    ON TWEET_ID OR ID OF THE DATAFRAME
    """
    # 1.

    def inspect(self, model):

        with self.session_scope() as s:

            for row in s.query(model).all():

                print("ROW; ", row)

    def update_by_tweetID(self, model, row):

        tweet_ID = str(row['tweet_id'])
        cluster_id = row['cluster']

        # connect to DB with session
        with self.session_scope() as s:

            """
            for row in s.query(model).filter(model.tweet_id == tweet_ID).all():

                print(f"ROW with {tweet_ID}", row)
            """
            s.query(model).filter(model.tweet_id == tweet_ID).update(
                {model.stdbscan_5000_4320_5: cluster_id})

            print('Updated tweet with ID{tweet_ID}!')

    def update_by_fishnetID(self, model, row):

        spat_temp_ID = str(row['spat_temp_id_str'])
        sig_words_dict = row['sig_words_dict']

        # connect to DB with session
        with self.session_scope() as s:

            """
            for row in s.query(model).filter(model.tweet_id == tweet_ID).all():

                print(f"ROW with {tweet_ID}", row)
            """
            s.query(model).filter(model.spat_temp_id_str == spat_temp_ID).update(
                {model.tfidf_bigrams_textcat: sig_words_dict})

            print(f'Updated tweet with ID{spat_temp_ID}!')

    def update_by_spattempID(self, model, row):

        spat_temp_ID = str(row['spat_temp_id_str'])
        sig_words_dict = row['sig_words_dict']

        # connect to DB with session
        with self.session_scope() as s:

            """
            for row in s.query(model).filter(model.tweet_id == tweet_ID).all():

                print(f"ROW with {tweet_ID}", row)
            """
            s.query(model).filter(model.spat_temp_id_str == spat_temp_ID).update(
                {model.tfidf_bigrams: sig_words_dict})

            print(f'Updated tweet with ID{spat_temp_ID}!')

    def update_textclassifier_tweetID(self, model, row):

        tweet_ID = str(row['tweet_id'])
        prediction = row['predictionJSON']

        # connect to DB with session
        with self.session_scope() as s:

            """
            for row in s.query(model).filter(model.tweet_id == tweet_ID).all():

                print(f"ROW with {tweet_ID}", row)
            """
            s.query(model).filter(model.tweet_id == tweet_ID).update(
                {model.classified_bow: prediction})

            print('Updated tweet with ID{tweet_ID}!')

    def update_fastcluster_tweetID(self, model, row):

        tweet_ID = str(row['tweet_id'])
        clusterID = row['cluster']

        print("type: ", type(clusterID))

        if math.isnan(clusterID):

            print('Cluster ID {tweet_ID} is NONE!')

        else:

            # connect to DB with session
            with self.session_scope() as s:

                """
                for row in s.query(model).filter(model.tweet_id == tweet_ID).all():

                    print(f"ROW with {tweet_ID}", row)
                """
                s.query(model).filter(model.tweet_id == tweet_ID).update(
                    {model.fastcluster_id_07: clusterID})

                print('Updated tweet with ID{tweet_ID}!')

    def update_by_stdbscanID(self, model, row):

        stdbscan_ID = row['stdbscan_id']
        sig_words_dict = row['sig_words_dict']

        # connect to DB with session
        with self.session_scope() as s:

            s.query(model).filter(model.stdbscan_id == stdbscan_ID).update(
                {model.tfidf_unigrams: sig_words_dict})

            print(f'Updated stdbscan cluster with ID{stdbscan_ID}!')

    # TRANSFORM AND LOAD
    # 2.

    def update_all(self, dataframe, model):

        # take each row
        for index, row in dataframe.iterrows():

            # call relevant update function
            self.update_by_fishnetID(model, row)

    @ contextmanager
    def session_scope(self):

        # local scope creates and uses a session
        session = self.Session()  # invokes sessionmaker.__call__()

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
