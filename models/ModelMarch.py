from sqlalchemy.types import ARRAY, Float, JSON, Text, TEXT
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY, Float
#from geoalchemy2 import Geometry

Base = declarative_base()

class March_Tweets(Base):
    __tablename__ = 'march_tweets'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    #final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION, nullable=True)
    # results of textClassifier
    tweet_score = Column(Integer, nullable=True)
    textclassifierjson = Column(JSON, nullable=True)
    classified_march = Column(String, nullable=True)

    # Constructor

    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_point_lat={}, tweet_score={}, textclassifierjson={}, classified_march={})>".format(self.tweet_id, self.text, self.created_at, self.final_point_lat, self.tweet_score, self.textclassifierjson, self.classified_march)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         #'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'tweet_score': self.tweet_score,
                         'textclassifierjson': self.textclassifierjson,
                         'classified_march': self.classified_march}

        return tweet_as_dict