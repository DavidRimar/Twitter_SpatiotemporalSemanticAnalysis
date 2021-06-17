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


class BristolFishnet(Base):
    __tablename__ = 'fishnet_11_5_sem'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    spat_temp_id = Column(Integer)
    spat_temp_id_str = Column(String)
    fishnet_id = Column(Integer)
    temp_day_id = Column(Integer)

    # Constructor

    def __repr__(self):
        return "<Tweet(spat_temp_id='{}', spat_temp_id_str='{}', fishnet_id={}, temp_day_id={})>".format(self.spat_temp_id, self.spat_temp_id_str, self.fishnet_id, self.temp_day_id)

    def as_dict(self):

        as_dict = {'spat_temp_id': self.spat_temp_id,
                   'spat_temp_id_str': self.spat_temp_id_str,
                   'fishnet_id': self.fishnet_id,
                   'temp_day_id': self.temp_day_id}

        return as_dict
