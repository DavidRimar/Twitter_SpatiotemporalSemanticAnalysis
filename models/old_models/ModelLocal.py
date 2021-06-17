from sqlalchemy.types import ARRAY, Float, JSON, Text, TEXT
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY, Float
from geoalchemy2 import Geometry

Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'stdbscan_results'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)
    text = Column(String)
    created_at = Column(DateTime)
    final_lon = Column(DOUBLE_PRECISION)
    final_lat = Column(DOUBLE_PRECISION)
    # final_point_astext = Column(Text)
    stdbscan_5000_30_2 = Column(Integer)

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_lon={}, final_lat={}, stdbscan_5000_30_2={})>".format(self.tweet_id, self.text, self.created_at, self.final_lon, self.final_lat, self.stdbscan_5000_30_2)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_lon': self.final_point_lon,
                         'final_lat': self.final_point_lat,
                         'stdbscan_5000_30_2': self.stdbscan_5000_30_2}

        return tweet_as_dict
