from datetime import datetime
import logging
import pickle
import sqlite3
from typing import *

import shapefile

from .meta import D, CREATE, INSERT

logger = logging.getLogger("dynageo")

SQLFILE = "data/ggs650.db"
ZIPCODES = "/home/smitty/proj/dynageo/dynageo/data/tl_2016_us_cd115"
LOAD_DATA = True  # False #


def dbInit():
    """We will blindly take all of the fields from the shapefile, and slap
         on some additional ones prior to producing a SQLite file from it.
    """
    print(SQLFILE)
    conn = sqlite3.connect(SQLFILE)
    with conn:
        c = conn.cursor()
        c.execute(CREATE)


def dbLoad():
    """We ETL data from the shapefile, merging the metadata with the
         shape_points into a SQLite table.
    """
    conn = sqlite3.connect(SQLFILE)
    with conn:
        r = shapefile.Reader(ZIPCODES).shapeRecords()
        print("shapes to process %s" % len(r))
        for d in r:
            print("shape record length %s" % len(d.record))
            [print("%s %s" % (x, y)) for x, y in enumerate(d.record)]
            bbox = d.shape.bbox
            points = (
                d.shape.points
            )  # TODO: load into collections.OrderedDict and pickle
            latMax = d.shape.bbox[3]
            latMin = d.shape.bbox[1]
            lonMax = d.shape.bbox[2]
            lonMin = d.shape.bbox[0]
            insert = INSERT % (
                d.record[D.STATEFP],
                d.record[D.CD115FP],
                d.record[D.GEOID],
                d.record[D.NAMELSAD],
                d.record[D.LSAD],
                d.record[D.CDSESSN],
                d.record[D.MTFCC],
                d.record[D.FUNCSTAT],
                d.record[D.ALAND],
                d.record[D.AWATER],
                d.record[D.INTPTLAT],
                d.record[D.INTPTLON],
                bbox,
                points,
                latMax,
                latMin,
                lonMax,
                lonMin,
            )
            conn.execute(insert)


if __name__ == "__main__":
    """Construct the database if invoked 
    """
    if LOAD_DATA:
        dbInit()
        dbLoad()
