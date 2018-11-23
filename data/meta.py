from enum import IntEnum


class D(IntEnum):
    STATEFP = 0
    CD115FP = 1
    GEOID = 2
    NAMELSAD = 3
    LSAD = 4
    CDSESSN = 5
    MTFCC = 6
    FUNCSTAT = 7
    ALAND = 8
    AWATER = 9
    INTPTLAT = 10
    INTPTLON = 11
    bbox = 12
    points = 13
    latMax = 14
    latMin = 15
    lonMax = 16
    lonMin = 17


CREATE = """CREATE TABLE dist (dist_id INTEGER PRIMARY KEY AUTOINCREMENT
, STATEFP,CD115FP,GEOID,NAMELSAD,LSAD
,CDSESSN,MTFCC,FUNCSTAT,ALAND,AWATER
,INTPTLAT,INTPTLON,bbox,points,latMax
,latMin,lonMax,lonMin);"""

SELECT = "SELECT * FROM dist;"

INSERT = """INSERT INTO dist (STATEFP,CD115FP,GEOID,NAMELSAD,LSAD
,CDSESSN,MTFCC,FUNCSTAT,ALAND,AWATER
,INTPTLAT,INTPTLON,bbox,points,latMax
,latMin,lonMax,lonMin)
VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s);"""

DYNOLOAD = "SELECT dist_id,latMax,latMin,lonMax,lonMin FROM dist;"
