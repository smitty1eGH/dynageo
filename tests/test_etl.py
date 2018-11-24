import sqlite3
from typing import *

import pytest

import shapefile


@pytest.fixture
def sqlMemC() -> sqlite3.Connection:
    """Connection to :memory:
    """
    return sqlite3.connect(':memory:')

@pytest.fixture
def dataPath() -> str:
    """Absolute path of shapefile to ingest
    """
    return "/home/smitty/proj/dynageo/dynageo/data/tl_2016_us_cd115"

@pytest.fixture
def xFields() -> List[str]:
    """In addition to the fields provided by the shapefile, we will also store
         - the provided bounding box point tuple
         - the points, which we will read into an OrderedDict and pickle
         - the explicit bounding box sides
    """
    return ['bbox','points','latMax','latMin','lonMax','lonMin']

@pytest.mark.skip("Scratch function for use in working on sqlite db.")
def test_dbInit_scratch(sqlMemC: sqlite3.Connection, dataPath :str, xFields :List[str]):
    """We are adding an autonumber field called dist_id, the given fields in the
         shapefile, and the additional management fields documented above.

       Publish to ~/data/meta.py the following:
         An enumeration of the fields
         CREATE TABLE sql
         SELECT sql
         INSERT sql
    """
    x=shapefile.Reader(dataPath)
    z=[y[0] for y in x.fields]
    z.pop(0) #Omit deletion flag
    z+=xFields
    a = ','.join([x for x in z])
    b = ['%s' for x in range(len(z))] 
    print("from enum import IntEnum")
    print("class D(IntEnum):")
    [print("    %s=%s" % (n,i)) for i,n in enumerate(z)]
    sql='"CREATE TABLE dist (dist_id INTEGER PRIMARY KEY AUTOINCREMENT, %s);"' % a
    print(sql)
    print('"SELECT * FROM dist;"')
    c=','.join(["d.record[D.%s]" % n for n in z])
    #maually quoted most of the VALUES
    print('"INSERT INTO dist (%s) VALUES (%s);" %% (%s)' % (a,','.join(b),c))

