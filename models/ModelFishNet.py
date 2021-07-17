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


class BristolFishnet_11_5(Base):
    __tablename__ = 'fishnet_11_5_sem'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    spat_temp_id = Column(Integer)
    spat_temp_id_str = Column(String)
    fishnet_id = Column(Integer)
    temp_day_id = Column(Integer)
    tfidf_topwords = Column(JSON)
    tfidf_topwords2 = Column(JSON)
    fishnet_geom_center = Column(Geometry('POINT'))
    fishnet_geom_center_lon = Column(DOUBLE_PRECISION)
    fishnet_geom_center_lat = Column(DOUBLE_PRECISION)
    time_day = Column(DateTime)
    tfidf_bigrams = Column(JSON)

    # Constructor

    def __repr__(self):
        return "<Tweet(spat_temp_id='{}', spat_temp_id_str='{}', fishnet_id={}, temp_day_id={}, tfidf_topwords={}, tfidf_topwords2={}, fishnet_geom_center={}, fishnet_geom_center_lon={}, fishnet_geom_center_lat={}, time_day={}, tfidf_bigrams={})>".format(self.spat_temp_id, self.spat_temp_id_str, self.fishnet_id, self.temp_day_id, self.tfidf_topwords, self.tfidf_topwords2, self.fishnet_geom_center, self.fishnet_geom_center_lon, self.fishnet_geom_center_lat, self.time_day, self.tfidf_bigrams)

    def as_dict(self):

        as_dict = {'spat_temp_id': self.spat_temp_id,
                   'spat_temp_id_str': self.spat_temp_id_str,
                   'fishnet_id': self.fishnet_id,
                   'temp_day_id': self.temp_day_id,
                   'tfidf_topwords': self.tfidf_topwords,
                   'tfidf_topwords2': self.tfidf_topwords2,
                   'fishnet_geom_center': self.fishnet_geom_center,
                   'fishnet_geom_center_lon': self.fishnet_geom_center_lon,
                   'fishnet_geom_center_lat': self.fishnet_geom_center_lat,
                   'time_day': self.time_day,
                   'tfidf_bigrams': self.tfidf_bigrams}

        return as_dict


class BristolFishnet_88_40(Base):
    __tablename__ = 'fishnet_88_40_sem'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    spat_temp_id = Column(Integer)
    spat_temp_id_str = Column(String)
    fishnet_id = Column(Integer)
    temp_day_id = Column(Integer)
    fishnet_geom_center = Column(Geometry('POINT'))
    fishnet_geom_center_lon = Column(DOUBLE_PRECISION)
    fishnet_geom_center_lat = Column(DOUBLE_PRECISION)
    time_day = Column(DateTime)
    tfidf_topwords = Column(JSON)
    tfidf_topwords_lem = Column(JSON)
    tfidf_bigrams = Column(JSON)

    # Constructor

    def __repr__(self):
        return "<Tweet(spat_temp_id='{}', spat_temp_id_str='{}', fishnet_id={}, temp_day_id={}, fishnet_geom_center={}, fishnet_geom_center_lon={}, fishnet_geom_center_lat={}, time_day={}, tfidf_topwords={}, tfidf_topwords_lem={}, tfidf_bigrams={})>".format(self.spat_temp_id, self.spat_temp_id_str, self.fishnet_id, self.temp_day_id, self.fishnet_geom_center, self.fishnet_geom_center_lon, self.fishnet_geom_center_lat, self.time_day, self.tfidf_topwords, self.tfidf_topwords_lem, self.tfidf_bigrams)

    def as_dict(self):

        as_dict = {'spat_temp_id': self.spat_temp_id,
                   'spat_temp_id_str': self.spat_temp_id_str,
                   'fishnet_id': self.fishnet_id,
                   'temp_day_id': self.temp_day_id,
                   'fishnet_geom_center': self.fishnet_geom_center,
                   'fishnet_geom_center_lon': self.fishnet_geom_center_lon,
                   'fishnet_geom_center_lat': self.fishnet_geom_center_lat,
                   'time_day': self.time_day,
                   'tfidf_topwords': self.tfidf_topwords,
                   'tfidf_topwords_lem': self.tfidf_topwords_lem,
                   'tfidf_bigrams': self.tfidf_bigrams}

        return as_dict
