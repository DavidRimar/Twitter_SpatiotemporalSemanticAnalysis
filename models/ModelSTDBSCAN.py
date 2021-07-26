from sqlalchemy.types import ARRAY, Float, JSON, Text, TEXT
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY, Float
from geoalchemy2 import Geometry

Base = declarative_base()

"""
Tweet Class (extends Base class)
Representation of the data schema of the tables related to
the 'Bristol riots' event in the PostgreSQL.
"""


class STDBSCAN_02_10800_3_SEM(Base):
    __tablename__ = 'stdbscan_02_10800_3_sem'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    stdbscan_id = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    convexhull = Column(Geometry)
    st_asgeojson = Column(JSON)
    bristol_textclassifier_70_volumes = Column(Integer)
    all_volumes = Column(Integer)
    normalized_volumes = Column(NUMERIC)
    scaled_vol_06 = Column(NUMERIC)
    span_day = Column(Integer)
    span_hour = Column(Integer)
    scaled_vol_1 = Column(NUMERIC)
    tfidf_bigrams = Column(JSON)
    tfidf_unigrams = Column(JSON)

    # Constructor

    def __repr__(self):
        return "<Tweet(stdbscan_id='{}', start_date='{}', end_date={}, convexhull={}, st_asgeojson={}, bristol_textclassifier_70_volumes={}, all_volumes={}, normalized_volumes{}, scaled_vol_06={}, span_day={}, span_hour={}, scaled_vol_1={}, tfidf_bigrams={}, tfidf_unigrams={})>".format(self.stdbscan_id, self.start_date, self.end_date, self.convexhull, self.st_asgeojson, self.bristol_textclassifier_70_volumes, self.all_volumes, self.normalized_volumes, self.scaled_vol_06, self.span_day, self.span_hour, self.scaled_vol_1, self.tfidf_bigrams, self.tfidf_unigrams)

    def as_dict(self):

        as_dict = {'stdbscan_id': self.stdbscan_id,
                   'start_date': self.start_date,
                   'end_date': self.end_date,
                   'convexhull': self.convexhull,
                   'st_asgeojson': self.st_asgeojson,
                   'bristol_textclassifier_70_volumes': self.bristol_textclassifier_70_volumes,
                   'all_volumes': self.all_volumes,
                   'normalized_volumes': self.normalized_volumes,
                   'scaled_vol_06': self.scaled_vol_06,
                   'span_day': self.span_day,
                   'span_hour': self.span_hours,
                   'scaled_vol_1': self.scaled_vol_1,
                   'tfidf_unigrams': self.tfidf_unigrams,
                   'tfidf_bigrams': self.tfidf_bigrams
                   }

        return as_dict
