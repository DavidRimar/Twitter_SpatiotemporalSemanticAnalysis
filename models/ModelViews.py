from sqlalchemy.types import ARRAY, Float, JSON, Text, TEXT
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY, Float
from geoalchemy2 import Geometry

Base = declarative_base()

"""
BristolView Class (extends Base class)
Representation of the data schema of bristol_plus_view materialized 
view in the PostgreSQL.
Keywords include: 
bristol protest riot march violence violent 
attack police officer bill scene fight disrupt siege
"""


class BristolView(Base):
    __tablename__ = 'bristol_view'
    id = Column(Integer)  # Auto-generated ID
    tweet_id = Column(String)
    text = Column(String)
    created_at = Column(DateTime)
    geo_coordinates_coords = Column(ARRAY(Float), nullable=True)
    geo_place_id = Column(String, nullable=True)
    final_geom_point = Column(Geometry('POINT'), nullable=True)
    final_geom_point_astext = Column(Text, nullable=True)
    final_geom_point_bgn = Column(Geometry('POINT'), nullable=True)

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, geo_coordinates_coords={}, geo_place_id={}, final_geom_point={}, final_geom_point_astext={}, final_geom_point_bgn={})>".format(self.tweet_id, self.text, self.created_at, self.geo_coordinates_coords, self.geo_place_id, self.final_geom_point, self.final_geom_point_astext, self.final_geom_point_bgn)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'geo_coordinates_coords': self.geo_coordinates_coords,
                         'geo_place_id': self.geo_place_id,
                         'final_geom_point': self.final_geom_point,
                         'final_geom_point_astext': self.final_geom_point_astext,
                         'final_geom_point_bgn': self.final_geom_point_bgn}

        return tweet_as_dict


class BristolViewV1(Base):
    __tablename__ = 'bristol_view_v1'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)
    text = Column(String)
    created_at = Column(DateTime)
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    final_point_astext = Column(Text)

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_point_lon={}, final_point_lat={}, final_point_astext={})>".format(self.tweet_id, self.text, self.created_at, self.final_point_lon, self.final_point_lat, self.final_point_astext)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'final_point_astext': self.final_point_astext}

        return tweet_as_dict
