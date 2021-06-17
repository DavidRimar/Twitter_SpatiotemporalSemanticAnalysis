from sqlalchemy.types import ARRAY, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY, Float
from geoalchemy2 import Geometry

Base = declarative_base()

"""
Tweet Class (extends Base class)
Representation of the data schema of 'Tweet' table in the PostgreSQL.
"""


class Tweet(Base):
    __tablename__ = 'tweets_geo'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    context_annotations = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime)  # (data.created_at)
    geo_place_id = Column(String, nullable=True)  # (includes.places.id)
    stream_rule_tag = Column(String)  # (matching_rules.tag)
    geom_points = Column(Geometry('POINT'), nullable=True)
    geom_points_astext = Column(String, nullable=True)
    geom_points_bgn = Column(Geometry('POINT'), nullable=True)  # TO BE ADDED

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', context_annotations={}, created_at={}, geo_place_id={}, stream_rule_tag={}, geom_points={}, geom_points_astext={}, geom_points_bgn={})>".format(self.tweet_id, self.text, self.context_annotations, self.created_at, self.geo_place_id, self.stream_rule_tag, self.geom_points, self.geom_points_astext, self.geom_points_bgn)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'context_annotations': self.context_annotations,
                         'created_at': self.created_at,
                         'geo_place_id': self.geo_place_id,
                         'stream_rule_tag': self.stream_rule_tag,
                         'geom_points': self.geom_points,
                         'geom_points_astext': self.geom_points_astext,
                         'geom_points_bgn': self.geom_points_bgn}

        return tweet_as_dict


class Place(Base):
    __tablename__ = 'places_geo'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    places_geo_place_id = Column(String)  # (includes.places.id)
    places_geo_bbox = Column(ARRAY(Float))  # (includes.places.geo.bbox)
    places_full_name = Column(String)  # (includes.places.full_name)
    places_place_type = Column(String)  # (includes.places.place_type)
    places_country_code = Column(String)  # (includes.places.country_code)

    # Constructor
    def __repr__(self):
        return "<Place(places_geo_place_id={}, places_geo_bbox={}, places_full_name={}, places_place_type={}, places_country_code={})>".format(self.places_geo_place_id, self.places_geo_bbox, self.places_full_name, self.places_place_type, self.places_country_code)
