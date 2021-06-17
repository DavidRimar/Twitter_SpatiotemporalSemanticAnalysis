from config import *
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import json
from models.ModelFishNet import *

"""
The TweetLoader class takes care of transforming the fields from a response
to adhere to the data schema represented by the Tweet class.
It uses sqlAlchemy to load the tweets to a DB.
"""


class FishNetLoader():

    # CONSTRUCTOR
    def __init__(self, database_url):

        # INSTANCE VARIABLES

        self.recreatedDB = False

        # an engine to communicate with PostgreSQL
        self.engine = create_engine(database_url)

        # a Session object to manage connections (session starts)
        self.Session = sessionmaker(bind=self.engine)

    ### METHODS ###

    # 1. start_load()
    # 2. transform_and_load()
    # 3. create_database()
    # 4. recreate_database()
    # 5. session_scope()

    # START LOAD
    # 1.
    def start_load(self, row_to_add):

        print("loading started!")

        """
        # if only interested in the new data, recreate_db deletes data streamed before
        if recreate_db == True and self.recreatedDB == False:
            self.recreate_database()
            print("recreate db ran")
            self.recreatedDB = True
        """

        # connect to DB with session
        with self.session_scope() as s:

            # add tweet to DB
            s.add(row_to_add)

            print("loading successful!")

    # TRANSFORM AND LOAD
    # 2.
    def transform_and_load(self, dataframe):

        spat_temp_id = 0
        spat_temp_id_str = ""
        fishnet_id = 0
        temp_day_id = 0
        pid = 0

        # iter every row in file
        # for loop
        for index, row in dataframe.iterrows():

            pid = index
            # print(pid)
            # print(type(pid))
            spat_temp_id = row["spat_temp_id"]
            spat_temp_id_str = row["spat_temp_id_str"]
            fishnet_id = row["fishnet_id"]
            temp_day_id = row["temp_day_id"]

            # inspect transformed Tweet() object
            # print("single_tweet: ", single_tweet)
            # construct tweet_data_dict
            as_dict = {'id': pid,
                       'spat_temp_id': spat_temp_id,
                       'spat_temp_id_str': spat_temp_id_str,
                       'fishnet_id': fishnet_id,
                       'temp_day_id': temp_day_id}

            # construct a Tweet() object
            # data passed in to Tweet() has to be in a dictionary format
            single_row = BristolFishnet(**as_dict)

            # print(single_row)
            # load data
            self.start_load(single_row)

    # RECREATE DATABASE
    # 4.
    def recreate_database(self):

        # drops all tables
        Base.metadata.drop_all(self.engine)

        # creates all tables
        Base.metadata.create_all(self.engine)

    # A CONTEXT MANAGER
    # 5.
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
