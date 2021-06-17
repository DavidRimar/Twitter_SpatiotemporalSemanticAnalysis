from sqlalchemy import create_engine
from datetime import datetime
# from TweetCollector_FullArchiveAPI.Tables import Base, Tweet, Place
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from contextlib import contextmanager
import json
# from Model import Tweet, Place
# from ModelTest import Tweet, Place
import pandas as pd

"""
The TweetCrawler class is responsible for query the DB.
"""


class TweetCrawler():

    ### CONSTRUCTOR ###
    def __init__(self, database_url):

        ### INSTANCE VARIABLES ###

        # an engine to communicate with PostgreSQL
        self.engine = create_engine(database_url)

        # a Session object to manage connections (session starts)
        self.Session = sessionmaker(bind=self.engine)

    ### METHODS ###

    """
    Queries Data from the database, with an SQL statement
    as an argument as string.
    """

    def crawl_data_with_session(self, model, filtering=None):

        # connect to DB with session
        with self.session_scope() as s:

            try:

                query_result = None
                df_query_result = {}

                if filtering == None:

                    # use session to get all rows
                    query_result = s.query(model).all()

                    print("Query ALL works!")

                    df_query_result = self.convert_results_to_df(query_result)

                    print("Query successful!")

                else:  # if filtering is not none

                    # use session to get rows with flter
                    query_result = s.query(model).filter(
                        model.fishnet_c_id == filtering).all()

                    print("Query wit Filter works!")

                    df_query_result = self.convert_results_to_df(query_result)

                    print("Query with filter successful!")

                # returns a list of 'Tweet's
                return df_query_result

            except:
                print("Error in the query!")

    """
    Queries Data from the database, with an SQL statement
    as an argument. (With connection)
    """

    def crawl_data_with_connection(self, statement):

        # query to be returned
        # query_object = None

        with self.engine.connect() as con:

            try:

                query_result = con.execute(statement)

                print("Query successful!")

                return query_result

            except:
                print("Error in the query!")

        # return the query object
        # return query_object

    """
    A context manager for the session.
    It ensures that all connections are closed.
    """
    # 2.
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

    def convert_results_to_df(self, query_result):

        records_df = {}

        if type(query_result) == list:  # if the query is made with session

            # builds a dataframe from each Tweet object as a row
            records_df = pd.DataFrame([tweet.as_dict()
                                       for tweet in query_result])

        else:  # if the query is made with connection
            df_textual_generic = pd.DataFrame(query_result.fetchall())
            df_textual_generic.columns = query_result.keys()
            records_df = df_textual_generic

        return records_df
