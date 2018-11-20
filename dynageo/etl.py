from datetime                   import datetime
import logging
import logging.config
import pickle
from typing                     import *

import shapefile
from sqlalchemy                 import create_engine
from sqlalchemy                 import Column, Integer, Float, String, DateTime, PickleType
from sqlalchemy.ext.declarative import declarative_base
from   sqlalchemy.orm    import sessionmaker
from   sqlalchemy.sql    import text

logging.config.fileConfig('logging.conf',disable_existing_loggers=False)
logger=logging.getLogger( 'sqlalchemy').setLevel(logging.DEBUG)
logger=logging.getLogger( 'dynageo')

SQLFILE  ='sqlite:///data/ggs664.sqlite'
ZIPCODES ="/home/smitty/proj/dynageo/dynageo/data/"
LOAD_DATA=True #False #
EXPORTDAT=True #False #

Base=declarative_base()
engine   = create_engine(SQLFILE, echo=True)
session  = sessionmaker(bind=engine)()
conn     = engine.connect()
#rawconn  = engine.raw_connection()

def load_data():
    '''We ETL data from the shapefile, merging the metadata with the
         shape_points into a SQLite table.
    '''
    for d in shapefile.Reader(ZIPCODES).shapeRecords():


if __name__=='__main__':
    '''Construct the database when invoked directly
    '''
    if LOAD_DATA: load_data()
    Base.metadata.create_all(engine)