
CREATE="""CREATE TABLE dist (dist_id INTEGER PRIMARY KEY AUTOINCREMENT
,DeletionFlag,STATEFP ,CD115FP ,GEOID   ,NAMELSAD
,LSAD        ,CDSESSN ,MTFCC   ,FUNCSTAT,ALAND
,AWATER      ,INTPTLAT,INTPTLON,bbox    ,points
,latMax      ,latMin  ,lonMax  ,lonMin);"""

SELECT="SELECT * FROM dist;"


def insert_dist(c,d):
    """C is the SQLite connection
       D is the district shape data
    """
INSERT INTO dist (DeletionFlag,STATEFP,CD115FP,GEOID,NAMELSAD,LSAD,CDSESSN,MTFCC,FUNCSTAT,ALAND,AWATER,INTPTLAT,INTPTLON,bbox,points,latMax,latMin,lonMax,lonMin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
