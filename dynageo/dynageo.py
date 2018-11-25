import hashlib
import logging
import logging.config
import struct
from typing import *
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UnicodeSetAttribute,
    UTCDateTimeAttribute,
)

logging.config.fileConfig("etc/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("dynageo")


def hash_sides(lat_u: float, lat_l: float, lon_w: float, lon_e: float) -> str:
    """Return sha256 hash of the values concatenated and converted to a string.
    """
    m = hashlib.sha256()
    m.update(
        b"%s_%s_%s_%s"
        % (
            struct.pack("f", lat_u),
            struct.pack("f", lat_l),
            struct.pack("f", lon_w),
            struct.pack("f", lon_e),
        )
    )
    return str(m.digest())


class Criteria:
    """Critera instance for running a query.
    """

    pass


class Results:
    """This is a convenience class for processing results from the index query.
    """

    pass


class BboxLatUIndex(GlobalSecondaryIndex):
    """LocalSecondaryIndex for lat_u attribute.
    """

    class Meta:
        index_name = "lat-u-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["rangestamp", "ids"])

    lat_u = NumberAttribute(hash_key=True)


class BboxLatLIndex(GlobalSecondaryIndex):
    """LocalSecondaryIndex for lat_l attribute.
    """

    class Meta:
        index_name = "lat-l-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["rangestamp", "ids"])

    lat_l = NumberAttribute(range_key=True)


class BboxLonWIndex(GlobalSecondaryIndex):
    """LocalSecondaryIndex for lon_w attribute.
    """

    class Meta:
        index_name = "lon-w-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["rangestamp", "ids"])

    lon_w = NumberAttribute(hash_key=True)


class BboxLonEIndex(GlobalSecondaryIndex):
    """LocalSecondaryIndex for lon_e attribute.
    """

    class Meta:
        index_name = "lon-e-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["rangestamp", "ids"])

    lon_e = NumberAttribute(hash_key=True)


class BboxElevIndex(LocalSecondaryIndex):
    """LocalSecondaryIndex for elev attribute.
    """

    class Meta:
        index_name = "elev-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["rangestamp", "ids"])

    hashkey = UnicodeAttribute(hash_key=True)
    elev = NumberAttribute(range_key=True)


class BboxSides(Model):
    """Model the sides and elevation of a bounding cube as a single table.
       The hashkey will be derived from the values of the sides
    """

    class Meta:
        table_name = "BboxSides"
        host = "http://localhost:8000"

    hashkey = UnicodeAttribute(hash_key=True)
    rangestamp = UTCDateTimeAttribute(range_key=True)
    lat_u = NumberAttribute(default=0)
    lat_l = NumberAttribute(default=0)
    lon_w = NumberAttribute(default=0)
    lon_e = NumberAttribute(default=0)
    # elev = NumberAttribute(default=0)
    ids = UnicodeSetAttribute(default=None)
    lat_u_index = BboxLatUIndex()
    lat_i_index = BboxLatLIndex()
    lon_w_index = BboxLonWIndex()
    lon_e_index = BboxLonEIndex()


# elev_index = BboxElevIndex()


if __name__ == "__main__":
    BboxSides.create_table(read_capacity_units=1, write_capacity_units=1)
