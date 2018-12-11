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


class DLoad(IntEnum):
    dist_id = 0
    latMax = 1
    latMin = 2
    lonMax = 3
    lonMin = 4


CREATE = """CREATE TABLE dist (dist_id INTEGER PRIMARY KEY AUTOINCREMENT
,STATEFP,CD115FP,GEOID,NAMELSAD,LSAD
,CDSESSN,MTFCC,FUNCSTAT,ALAND,AWATER
,INTPTLAT,INTPTLON,bbox,points,latMax
,latMin,lonMax,lonMin);"""

SELECT = "SELECT * FROM dist;"

INSERT = """INSERT INTO dist (STATEFP,CD115FP,GEOID,NAMELSAD,LSAD
,CDSESSN,MTFCC,FUNCSTAT,ALAND,AWATER
,INTPTLAT,INTPTLON,bbox,points,latMax
,latMin,lonMax,lonMin)
VALUES ('%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s', '%s','%s','%s','%s',%s, %s,%s,%s);"""

DYNOLOAD = "SELECT dist_id,latMax,latMin,lonMax,lonMin FROM dist;"

UBERBBOX = """SELECT 0,"   ", " Latitude ", " Longitude"
UNION
SELECT 1,"---", "----------", "-----------"
UNION
SELECT 2,"Max", " " || (SELECT max(latMax) FROM dist), " " || (SELECT max(lonMax) FROM dist)
UNION
SELECT 3,"Min", (SELECT min(latMin) FROM dist), (SELECT min(lonMin) FROM dist);"""

CONUS = """SELECT "Continental U.S.: " || count(dist_id)
FROM   dist
WHERE (latMin >   25) AND (latMax <  50) 
  AND (lonMin > -125) AND (lonMax < -66);"""
