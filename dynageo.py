import hashlib
import logging
import logging.config
from typing import *
from pynamodb.models import Model
from pynamodb.indexes import LocalSecondaryIndex, IncludeProjection
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

logging.config.fileConfig("etc/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("dynageo")

class BboxSides(Model):
    '''Model the sides of a bounding box as a single table.
       The hashkey will be derived from the values of the sides
    '''
    class Meta:
        table_name = 'dynageo'

    hashkey = UnicodeAttribute(hash_key=True)
    rangestamp = UTCDateTimeAttribute(range_key=True)
    lat_u = NumberAttribute(default=0)
    lat_l = NumberAttribute(default=0)
    lon_w = NumberAttribute(default=0)
    lon_e = NumberAttribute(default=0)
    ids = UnicodeSetAttribute(default=None)

class BboxLatUIndex(LocalSecondaryIndex):
    '''LocalSecondaryIndex for lat_u attribute.
    '''
    class Meta:
        index_name = 'lat-u-index'
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection()

def hash_sides(lat_u: float, lat_l: float, lon_w: float, lon_e :float):
    '''Return sha256 hash of the values concatenated and converted to a byte string. 
    '''
    m = hashlib.sha256()
    m.update(b"%s_%s_%s_%s" % (lat_u,lat_l,lon_w,lon_e))
    return m.digest()



if __name__ == "__main__":
    logger.debug("Hello, world!")
