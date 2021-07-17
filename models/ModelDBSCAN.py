from sqlalchemy.types import ARRAY, Float, JSON, Text, TEXT
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
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


class BristolDBSCAN_004_5(Base):
    __tablename__ = 'dbscan_004_5_sem'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    spat_temp_id = Column(Integer)
    spat_temp_id_str = Column(String)
    dbscan_004_5_temp_id = Column(Integer)
    temp_day_id = Column(Integer)
    tfidf_topwords_lem = Column(JSON)
    tfidf_bigrams = Column(JSON)
    convexhull = Column(Geometry)

    # Constructor

    def __repr__(self):
        return "<Tweet(spat_temp_id='{}', spat_temp_id_str='{}', dbscan_004_5_temp_id={}, temp_day_id={}, tfidf_topwords_lem={}, tfidf_bigrams={}, convexhull={})>".format(self.spat_temp_id, self.spat_temp_id_str, self.dbscan_004_5_temp_id, self.temp_day_id, self.tfidf_topwords_lem, self.tfidf_bigrams, self.convexhull)

    def as_dict(self):

        as_dict = {'spat_temp_id': self.spat_temp_id,
                   'spat_temp_id_str': self.spat_temp_id_str,
                   'dbscan_004_5_temp_id': self.dbscan_004_5_temp_id,
                   'temp_day_id': self.temp_day_id,
                   'tfidf_topwords_lem': self.tfidf_topwords_lem,
                   'tfidf_bigrams': self.tfidf_bigrams,
                   'convexhull': self.convexhull}

        return as_dict
