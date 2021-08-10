from sqlalchemy.types import ARRAY, Float, JSON, Text, TEXT
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY, Float
#from geoalchemy2 import Geometry

Base = declarative_base()

"""
Tweet Class (extends Base class)
Representation of the data schema of the tables related to
the 'Bristol riots' event in the PostgreSQL.
"""


class BristolSEM(Base):
    __tablename__ = 'bristol_sem'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    tweet_score = Column(Integer)

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, tweet_score={})>".format(self.tweet_id, self.text, self.created_at, self.tweet_score)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'tweet_score': self.tweet_score}

        return tweet_as_dict


class BristolST(Base):
    __tablename__ = 'bristol_st'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    final_point_astext = Column(Text)
    # STDBSCAN VARIATIONS (meter_minutes_minpts)
    # 3 DAY (4320 minutes)
    stdbscan_5000_4320_5 = Column(Integer, nullable=True)
    stdbscan_3500_4320_5 = Column(Integer, nullable=True)
    stdbscan_2500_4320_5 = Column(Integer, nullable=True)
    stdbscan_6000_4320_5 = Column(Integer, nullable=True)

    # 6 DAY (8640 minutes)
    stdbscan_5000_8640_2 = Column(Integer, nullable=True)
    stdbscan_3500_8640_2 = Column(Integer, nullable=True)
    stdbscan_2500_8640_2 = Column(Integer, nullable=True)
    stdbscan_1000_8640_2 = Column(Integer, nullable=True)

    # GEOMETRIC COLUMNS (bng)

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_point_lon={}, final_point_lat={}, final_point_astext={}, stdbscan_5000_4320_5={}, stdbscan_3500_4320_5={}, stdbscan_2500_4320_5={}, stdbscan_6000_4320_5={}, stdbscan_5000_8640_2={}, stdbscan_3500_8640_2={}, stdbscan_2500_8640_2={}, stdbscan_1000_8640_2={})>".format(self.tweet_id, self.text, self.created_at, self.final_point_lon, self.final_point_lat, self.final_point_astext, self.stdbscan_5000_4320_5, self.stdbscan_3500_4320_5, self.stdbscan_2500_4320_5, self.stdbscan_6000_4320_5, self.stdbscan_5000_8640_2, self.stdbscan_3500_8640_2, self.stdbscan_2500_8640_2, self.stdbscan_1000_8640_2)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'final_point_astext': self.final_point_astext,
                         'stdbscan_5000_4320_5': self.stdbscan_5000_4320_5,
                         'stdbscan_3500_4320_5': self.stdbscan_3500_4320_5,
                         'stdbscan_5000_4320_5': self.stdbscan_2500_4320_5,
                         'stdbscan_6000_4320_5': self.stdbscan_6000_4320_5,
                         'stdbscan_5000_8640_2': self.stdbscan_5000_8640_2,
                         'stdbscan_3500_8640_2': self.stdbscan_3500_8640_2,
                         'stdbscan_2500_8640_2': self.stdbscan_2500_8640_2,
                         'stdbscan_1000_8640_2': self.stdbscan_1000_8640_2}

        return tweet_as_dict


class BristolSet2ST(Base):
    __tablename__ = 'bristol_set2_st'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_geom_point_4326 = Column(Geometry('POLYGON'))
    final_geom_point_astext = Column(Text)
    final_geom_point_bng = Column(Geometry('POLYGON'))
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)

    # STDBSCAN VARIATIONS (meter_minutes_minpts)
    # 3 DAY (4320 minutes)
    stdbscan_01_3600_5 = Column(Integer, nullable=True)

    fastcluster_id_07 = Column(Integer)

    # Constructor

    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_geom_point_4326={}, final_geom_point_astext={}, final_geom_point_bng={}, final_point_lon={}, final_point_lat={}, stdbscan_01_3600_5={}, fastcluster_id_07={})>".format(self.tweet_id, self.text, self.created_at, self.final_geom_point_4326, self.final_geom_point_astext, self.final_geom_point_bng,  self.final_point_lon, self.final_point_lat, self.stdbscan_01_3600_5, self.fastcluster_id_07)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_geom_point_4326': self.final_geom_point_4326,
                         'final_geom_point_astext': self.final_geom_point_astext,
                         'final_geom_point_bng': self.final_geom_point_bng,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'stdbscan_01_3600_5': self.stdbscan_01_3600_5,
                         'fastcluster_id_07': self.fastcluster_id_07}

        return tweet_as_dict


class BristolSet2FishNet(Base):
    __tablename__ = 'bristol_set2_fishnet'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_geom_point_4326 = Column(Geometry('POLYGON'))
    final_geom_point_astext = Column(Text)
    final_geom_point_bng = Column(Geometry('POLYGON'))
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    fishnet_c_id = Column(Integer, nullable=True)

    # STDBSCAN VARIATIONS (meter_minutes_minpts)
    # 3 DAY (4320 minutes)
    # stdbscan_5000_4320_5 = Column(Integer, nullable=True)
    #stdbscan_3500_4320_5 = Column(Integer, nullable=True)
    #stdbscan_2500_4320_5 = Column(Integer, nullable=True)
    #stdbscan_6000_4320_5 = Column(Integer, nullable=True)

    # 6 DAY (8640 minutes)
    #stdbscan_5000_8640_2 = Column(Integer, nullable=True)
    #stdbscan_3500_8640_2 = Column(Integer, nullable=True)
    #stdbscan_2500_8640_2 = Column(Integer, nullable=True)
    #stdbscan_1000_8640_2 = Column(Integer, nullable=True)

    # GEOMETRIC COLUMNS (bng)

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_geom_point_4326={}, final_geom_point_astext={}, final_geom_point_bng={}, final_point_lon={}, final_point_lat={}, fishnet_c_id={})>".format(self.tweet_id, self.text, self.created_at, self.final_geom_point_4326, self.final_geom_point_astext, self.final_geom_point_bng,  self.final_point_lon, self.final_point_lat, self.fishnet_c_id)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_geom_point_4326': self.final_geom_point_4326,
                         'final_geom_point_astext': self.final_geom_point_astext,
                         'final_geom_point_bng': self.final_geom_point_bng,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'fishnet_c_id': self.fishnet_c_id}

        return tweet_as_dict


class BristolFishNet_11_5(Base):
    __tablename__ = 'bristol_fishnet_11_5_temp'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_geom_point_4326 = Column(Geometry('POLYGON'))
    final_geom_point_astext = Column(Text)
    final_geom_point_bng = Column(Geometry('POLYGON'))
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    fishnet_c_id = Column(Integer, nullable=True)
    temp_day_id = Column(Integer, nullable=True)

    # STDBSCAN VARIATIONS (meter_minutes_minpts)
    # 3 DAY (4320 minutes)
    # stdbscan_5000_4320_5 = Column(Integer, nullable=True)
    #stdbscan_3500_4320_5 = Column(Integer, nullable=True)
    #stdbscan_2500_4320_5 = Column(Integer, nullable=True)
    #stdbscan_6000_4320_5 = Column(Integer, nullable=True)

    # 6 DAY (8640 minutes)
    #stdbscan_5000_8640_2 = Column(Integer, nullable=True)
    #stdbscan_3500_8640_2 = Column(Integer, nullable=True)
    #stdbscan_2500_8640_2 = Column(Integer, nullable=True)
    #stdbscan_1000_8640_2 = Column(Integer, nullable=True)

    # GEOMETRIC COLUMNS (bng)

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_geom_point_4326={}, final_geom_point_astext={}, final_geom_point_bng={}, final_point_lon={}, final_point_lat={}, fishnet_c_id={}, temp_day_id={})>".format(self.tweet_id, self.text, self.created_at, self.final_geom_point_4326, self.final_geom_point_astext, self.final_geom_point_bng,  self.final_point_lon, self.final_point_lat, self.fishnet_c_id, self.temp_day_id)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_geom_point_4326': self.final_geom_point_4326,
                         'final_geom_point_astext': self.final_geom_point_astext,
                         'final_geom_point_bng': self.final_geom_point_bng,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'fishnet_c_id': self.fishnet_c_id,
                         'temp_day_id': self.temp_day_id}

        return tweet_as_dict


class BristolFishNet_88_40(Base):
    __tablename__ = 'bristol_fishnet_88_40_temp'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_geom_point_4326 = Column(Geometry('POLYGON'))
    final_geom_point_astext = Column(Text)
    final_geom_point_bng = Column(Geometry('POLYGON'))
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    fishnet_c_id = Column(Integer, nullable=True)
    temp_day_id = Column(Integer, nullable=True)

    # GEOMETRIC COLUMNS (bng)

    # Constructor
    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_geom_point_4326={}, final_geom_point_astext={}, final_geom_point_bng={}, final_point_lon={}, final_point_lat={}, fishnet_c_id={}, temp_day_id={})>".format(self.tweet_id, self.text, self.created_at, self.final_geom_point_4326, self.final_geom_point_astext, self.final_geom_point_bng,  self.final_point_lon, self.final_point_lat, self.fishnet_c_id, self.temp_day_id)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_geom_point_4326': self.final_geom_point_4326,
                         'final_geom_point_astext': self.final_geom_point_astext,
                         'final_geom_point_bng': self.final_geom_point_bng,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'fishnet_c_id': self.fishnet_c_id,
                         'temp_day_id': self.temp_day_id}

        return tweet_as_dict


class Bristol_Set2_DBSCAN(Base):
    __tablename__ = 'bristol_set2_dbscan'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_geom_point_4326 = Column(Geometry('POLYGON'))
    final_geom_point_astext = Column(Text)
    final_geom_point_bng = Column(Geometry('POLYGON'))
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    # DBSCAN IDs (entire time window)
    dbscan_005_5 = Column(Integer)
    dbscan_002_5 = Column(Integer)
    dbscan_001_5 = Column(Integer)
    dbscan_0005_5 = Column(Integer)
    temp_day_id = Column(Integer, nullable=True)
    # DBSCAN IDs (per day)
    dbscan_002_5_temp = Column(Integer)
    dbscan_004_5_temp = Column(Integer)

    # GEOMETRIC COLUMNS (bng)

    # Constructor

    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_geom_point_4326={}, final_geom_point_astext={}, final_geom_point_bng={}, final_point_lon={}, final_point_lat={}, dbscan_005_5={}, dbscan_002_5={}, dbscan_001_5={}, dbscan_0005_5={}, temp_day_id={}, dbscan_002_5_temp={}, dbscan_004_5_temp={})>".format(self.tweet_id, self.text, self.created_at, self.final_geom_point_4326, self.final_geom_point_astext, self.final_geom_point_bng,  self.final_point_lon, self.final_point_lat, self.dbscan_005_5, self.dbscan_002_5, self.dbscan_001_5, self.dbscan_0005_5, self.temp_day_id, self.dbscan_002_5_temp, self.dbscan_004_5_temp)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_geom_point_4326': self.final_geom_point_4326,
                         'final_geom_point_astext': self.final_geom_point_astext,
                         'final_geom_point_bng': self.final_geom_point_bng,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'dbscan_005_5': self.dbscan_005_5,
                         'dbscan_002_5': self.dbscan_002_5,
                         'dbscan_001_5': self.dbscan_001_5,
                         'dbscan_0005_5': self.dbscan_0005_5,
                         'temp_day_id': self.temp_day_id,
                         'dbscan_002_5_temp': self.dbscan_002_5_temp,
                         'dbscan_004_5_temp': self.dbscan_004_5_temp}

        return tweet_as_dict


class Bristol_Set2_TextClassifier(Base):
    __tablename__ = 'bristol_set2_textclassifier'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_geom_point_4326 = Column(Geometry('POLYGON'))
    final_geom_point_astext = Column(Text)
    final_geom_point_bng = Column(Geometry('POLYGON'))
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    # results of textClassifier
    tweet_score = Column(Integer)
    textclassifierjson = Column(JSON)
    classified_bow = Column(JSON)

    # Constructor

    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_geom_point_4326={}, final_geom_point_astext={}, final_geom_point_bng={}, final_point_lon={}, final_point_lat={}, tweet_score={}, textclassifierjson={}, classified_bow={})>".format(self.tweet_id, self.text, self.created_at, self.final_geom_point_4326, self.final_geom_point_astext, self.final_geom_point_bng,  self.final_point_lon, self.final_point_lat, self.tweet_score, self.textclassifierjson, self.classified_bow)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_geom_point_4326': self.final_geom_point_4326,
                         'final_geom_point_astext': self.final_geom_point_astext,
                         'final_geom_point_bng': self.final_geom_point_bng,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'tweet_score': self.tweet_score,
                         'textclassifierjson': self.textclassifierjson,
                         'classified_bow': self.classified_bow}

        return tweet_as_dict


class Bristol_Set2_TextClassifier_70(Base):
    __tablename__ = 'bristol_set2_textclassifier_70'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_geom_point_4326 = Column(Geometry('POLYGON'))
    final_geom_point_astext = Column(Text)
    final_geom_point_bng = Column(Geometry('POLYGON'))
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    # results of textClassifier
    tweet_score = Column(Integer)
    textclassifierjson = Column(JSON)
    stdbscan_02_10800_3 = Column(Integer)
    stdbscan_03_10800_3 = Column(Integer)
    stdbscan_01_10800_3 = Column(Integer)
    temp_day_id = Column(Integer)
    fishnet_c_id = Column(Integer)

    # Constructor

    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_geom_point_4326={}, final_geom_point_astext={}, final_geom_point_bng={}, final_point_lon={}, final_point_lat={}, tweet_score={}, textclassifierjson={}, stdbscan_02_10800_3={}, stdbscan_03_10800_3={}, stdbscan_01_10800_3={}, temp_day_id={}, fishnet_c_id={})>".format(self.tweet_id, self.text, self.created_at, self.final_geom_point_4326, self.final_geom_point_astext, self.final_geom_point_bng,  self.final_point_lon, self.final_point_lat, self.tweet_score, self.textclassifierjson, self.stdbscan_02_10800_3, self.stdbscan_03_10800_3, self.stdbscan_01_10800_3, self.temp_day_id, self.fishnet_c_id)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_geom_point_4326': self.final_geom_point_4326,
                         'final_geom_point_astext': self.final_geom_point_astext,
                         'final_geom_point_bng': self.final_geom_point_bng,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'tweet_score': self.tweet_score,
                         'textclassifierjson': self.textclassifierjson,
                         'stdbscan_02_10800_3': self.stdbscan_02_10800_3,
                         'stdbscan_03_10800_3': self.stdbscan_03_10800_3,
                         'stdbscan_01_10800_3': self.stdbscan_01_10800_3,
                         'temp_day_id': self.temp_day_id,
                         'fishnet_c_id': self.fishnet_c_id}

        return tweet_as_dict


"""
class March_Tweets(Base):
    __tablename__ = 'march_tweets'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    tweet_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    created_at = Column(DateTime)  # (data.created_at)
    final_point_lon = Column(DOUBLE_PRECISION)
    final_point_lat = Column(DOUBLE_PRECISION)
    # results of textClassifier
    tweet_score = Column(Integer)
    textclassifierjson = Column(JSON)

    # Constructor

    def __repr__(self):
        return "<Tweet(tweet_id='{}', text='{}', created_at={}, final_point_lon={}, final_point_lat={}, tweet_score={}, textclassifierjson={})>".format(self.tweet_id, self.text, self.created_at, self.final_point_lon, self.final_point_lat, self.tweet_score, self.textclassifierjson)

    def as_dict(self):

        tweet_as_dict = {'tweet_id': self.tweet_id,
                         'text': self.text,
                         'created_at': self.created_at,
                         'final_point_lon': self.final_point_lon,
                         'final_point_lat': self.final_point_lat,
                         'tweet_score': self.tweet_score,
                         'textclassifierjson': self.textclassifierjson}

        return tweet_as_dict
"""