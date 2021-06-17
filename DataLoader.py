from config import *
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import json
from sqlalchemy import update


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

    # TRANSFORM AND LOAD
    # 2.

    def update_all(self, dataframe, model):

        # take each row
        for index, row in dataframe.iterrows():

            # call
            self.update_by_tweetID(model, row)

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
