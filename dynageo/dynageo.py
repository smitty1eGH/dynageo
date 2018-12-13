import hashlib
import logging
import logging.config
import struct
from typing import *

from pynamodb.connection import Connection
from pynamodb.models import Model
from pynamodb.indexes import (
    GlobalSecondaryIndex,
    LocalSecondaryIndex,
    IncludeProjection,
)
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UnicodeSetAttribute,
    UTCDateTimeAttribute,
)

from data.meta import DLoad

logging.config.fileConfig("etc/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("dynamodb")
logger.setLevel(logging.DEBUG)
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
    TASK:
      ingest bounding box corner points
      break them down into index query criteria
      run queries against each of the four indices
      process the results using sets
    """

    def __init__(self, lat_u, lat_l, lon_w, lon_e):
        """TODO: add a constructor accepting points.
        """
        self.lat_u = lat_u
        self.lat_l = lat_l
        self.lon_w = lon_w
        self.lon_e = lon_e

    def query(self, bbox_sides):
        """The high-level API failed. The low-level API works, but you have to understand that the dispatch() method that calls through botocore out to the API is in fact a generator returning a list of dicts representing the ATTRIBUTES_TO_GET.
           Do a dictionary lookup in a list comprehension so that RESP is a List[str] of ids (could someday be .csv).
           Build frozen sets of the response against self for later reduction.

           TODO: We'd also like to make the conditions work as BETWEEN operators, so that we can identify ids which only cross one of the bounding box sides.
                 Later reductions would examine the shape list and area, so that we could craft a rule, for example:
                 "This bounding box, and anything which is 50% contained in it."

                 Or, a list of tuples with ID and percentage containment.
        """
        conn = Connection()

        condition = NumberAttribute(attr_name="lat_u") <= self.lat_u
        resp = [
            x["ids"]["S"]
            for x in conn.rate_limited_scan(
                "BboxSides",
                filter_condition=condition,
                attributes_to_get=["ids"],
                index_name="lat-u-index",
            )
        ]
        self.lat_u_ids = frozenset(resp)

        condition = self.lat_l <= NumberAttribute(attr_name="lat_l")
        resp = [
            x["ids"]["S"]
            for x in conn.rate_limited_scan(
                "BboxSides",
                filter_condition=condition,
                attributes_to_get=["ids"],
                index_name="lat-l-index",
            )
        ]
        self.lat_l_ids = frozenset(resp)

        condition = NumberAttribute(attr_name="lon_w") <= self.lon_w
        resp = [
            x["ids"]["S"]
            for x in conn.rate_limited_scan(
                "BboxSides",
                filter_condition=condition,
                attributes_to_get=["ids"],
                index_name="lon-w-index",
            )
        ]
        self.lon_w_ids = frozenset(resp)

        condition = self.lon_e <= NumberAttribute(attr_name="lon_e")
        resp = [
            x["ids"]["S"]
            for x in conn.rate_limited_scan(
                "BboxSides",
                filter_condition=condition,
                attributes_to_get=["ids"],
                index_name="lon-e-index",
            )
        ]
        self.lon_e_ids = frozenset(resp)

        logger.debug("query complete")

    def reduce(self):
        """Go through the frozen set results from self.query() and discover the internals.

           TODO: derive a self.partially_contained
        """
        self.contained = self.lat_u_ids.intersection(
            self.lat_l_ids, self.lon_w_ids, self.lon_e_ids
        )
        #       logger.debug("id sets: lat_u %s\n\tlat_l %s\n\tlon_w %s\n\tlon_e %s",self.lat_u_ids,self.lat_l_ids,self.lon_w_ids,self.lon_e_ids)
        #       logger.debug("merged: lat_u,lat_l %s",self.lat_u_ids.intersection(self.lat_l_ids))
        #       logger.debug("merged: lon_w,lon_e %s",self.lon_w_ids.intersection(self.lon_e_ids))
        return self.contained


class BboxLatUIndex(GlobalSecondaryIndex):
    """LocalSecondaryIndex for lat_u attribute.
    """

    class Meta:
        index_name = "lat-u-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["ids", "lat_u"])

    ids = UnicodeAttribute(hash_key=True, default="-")
    rangestamp = UTCDateTimeAttribute(range_key=True)


class BboxLatLIndex(GlobalSecondaryIndex):
    """LocalSecondaryIndex for lat_l attribute.
    """

    class Meta:
        index_name = "lat-l-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["lat_l"])

    ids = UnicodeAttribute(hash_key=True, default=0)
    rangestamp = UTCDateTimeAttribute(range_key=True)


class BboxLonWIndex(GlobalSecondaryIndex):
    """LocalSecondaryIndex for lon_w attribute.
    """

    class Meta:
        index_name = "lon-w-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["lon_w"])

    ids = UnicodeAttribute(hash_key=True, default=0)
    rangestamp = UTCDateTimeAttribute(range_key=True)


class BboxLonEIndex(GlobalSecondaryIndex):
    """LocalSecondaryIndex for lon_e attribute.
    """

    class Meta:
        index_name = "lon-e-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(["lon_e"])

    ids = UnicodeAttribute(hash_key=True, default=0)
    rangestamp = UTCDateTimeAttribute(range_key=True)


# class BboxElevIndex(LocalSecondaryIndex):
#    """LocalSecondaryIndex for elev attribute.
#    """
#
#    class Meta:
#        index_name = "elev-index"
#        read_capacity_units = 2
#        write_capacity_units = 1
#        projection = IncludeProjection(["rangestamp", "ids"])
#
#    hashkey = UnicodeAttribute(hash_key=True)
#    rangestamp = UTCDateTimeAttribute(range_key=True)


class BboxSides(Model):
    """Model the sides and elevation of a bounding cube as a single table.
       The hashkey will be derived from the values of the sides
    """

    class Meta:
        table_name = "BboxSides"
        region = "us-east-1"
        host = "http://localhost:8000"

    hashkey = UnicodeAttribute(hash_key=True)
    rangestamp = UTCDateTimeAttribute(range_key=True)
    lat_u = NumberAttribute(default=0)
    lat_l = NumberAttribute(default=0)
    lon_w = NumberAttribute(default=0)
    lon_e = NumberAttribute(default=0)
    ids = UnicodeAttribute(default="-")
    lat_u_index = BboxLatUIndex()
    lat_l_index = BboxLatLIndex()
    lon_w_index = BboxLonWIndex()
    lon_e_index = BboxLonEIndex()

    # elev = NumberAttribute(default=0)


# elev_index = BboxElevIndex()


if __name__ == "__main__":
    # BboxSides.create_table(read_capacity_units=1, write_capacity_units=1)
    conn = Connection()
    condition = NumberAttribute(attr_name="lat_u") <= k_crit[DLoad.latMax]
    resp = conn.rate_limited_scan(
        "BboxSides",
        filter_condition=condition,
        attributes_to_get=["ids"],
        index_name="lat-u-index",
    )
    for x in resp:
        print(x)
