import hashlib
import logging
import logging.config
from typing import *
from pynamodb.models import Model
from pynamodb.indexes import LocalSecondaryIndex, IncludeProjection
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UnicodeSetAttribute,
    UTCDateTimeAttribute,
)

logging.config.fileConfig("etc/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("dynageo")


def hash_sides(
    lat_u: float, lat_l: float, lon_w: float, lon_e: float, elev: float = 0.0
):
    """Return sha256 hash of the values concatenated and converted to a byte string. 
    """
    m = hashlib.sha256()
    m.update(b"%s_%s_%s_%s" % (lat_u, lat_l, lon_w, lon_e))
    return m.digest()


class Criteria:
    """Critera instance for running a query.
    """

    pass


class Results:
    """This is a convenience class for processing results from the index query.
    """

    pass


def load_bboxes() -> int:
    """Populate the bounding box table make it a batch job.
       Return the number of records inserted.
    """
    pass


def query_bboxes(c: Criteria) -> Results:
    """Query the table. Break the Criteria out against the indices. Load the returns
         into the Results.
    """
    pass


class BboxLatUIndex(LocalSecondaryIndex):
    """LocalSecondaryIndex for lat_u attribute.
    """

    class Meta:
        index_name = "lat-u-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(rangestamp, ids)

    hashkey = UnicodeAttribute(hash_key=True)
    lat_u = NumberAttribute(range_key=True)


class BboxLatLIndex(LocalSecondaryIndex):
    """LocalSecondaryIndex for lat_l attribute.
    """

    class Meta:
        index_name = "lat-l-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(rangestamp, ids)

    hashkey = UnicodeAttribute(hash_key=True)
    lat_l = NumberAttribute(range_key=True)


class BboxLonWIndex(LocalSecondaryIndex):
    """LocalSecondaryIndex for lon_w attribute.
    """

    class Meta:
        index_name = "lon-w-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(rangestamp, ids)

    hashkey = UnicodeAttribute(hash_key=True)
    lon_w = NumberAttribute(range_key=True)


class BboxLonEIndex(LocalSecondaryIndex):
    """LocalSecondaryIndex for lon_e attribute.
    """

    class Meta:
        index_name = "lon-e-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(rangestamp, ids)

    hashkey = UnicodeAttribute(hash_key=True)
    lon_e = NumberAttribute(range_key=True)


class BboxElevIndex(LocalSecondaryIndex):
    """LocalSecondaryIndex for elev attribute.
    """

    class Meta:
        index_name = "elev-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(rangestamp, ids)

    hashkey = UnicodeAttribute(hash_key=True)
    elev = NumberAttribute(range_key=True)


class BboxSides(Model):
    """Model the sides and elevation of a bounding cube as a single table.
       The hashkey will be derived from the values of the sides
    """

    class Meta:
        table_name = "dynageo"
        host = "http://localhost:8000"

    hashkey = UnicodeAttribute(hash_key=True)
    rangestamp = UTCDateTimeAttribute(range_key=True)
    lat_u = NumberAttribute(default=0)
    lat_l = NumberAttribute(default=0)
    lon_w = NumberAttribute(default=0)
    lon_e = NumberAttribute(default=0)
    elev = NumberAttribute(default=0)
    ids = UnicodeSetAttribute(default=None)
    lat_u_index = BboxLatUIndex()
    lat_i_index = BboxLatLIndex()
    lon_w_index = BboxLonWIndex()
    lon_e_index = BboxLonEIndex()
    elev_index = BboxElevIndex()


if __name__ == "__main__":
    BboxSides.create_table(read_capacity_units=1, write_capacity_units=1)
