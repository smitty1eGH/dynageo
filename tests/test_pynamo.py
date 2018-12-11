import inspect
import sqlite3
from typing import List


from pynamodb.connection import Connection

from pynamodb.attributes import NumberAttribute, UTCDateTimeAttribute
from pynamodb.expressions.condition import Comparison
import pytest

from dynageo.dynageo import BboxSides, Criteria
from data.meta import DLoad


@pytest.fixture
def kentucky() -> str:
    """Returns [22,65,106,144,176,204]
    """
    return """SELECT dist_id
              FROM   dist
              WHERE (latMin >=  36.26) AND (latMax <=  39.25)
                AND (lonMin >= -89.60) AND (lonMax <= -81.35);"""


@pytest.fixture
def k_crit() -> List[float]:
    return [0.0, 39.25, 36.26, -89.60, -81.35]


@pytest.mark.skip
def test_sqlite_kentucky(kentucky: str):
    conn = sqlite3.connect("data/ggs650.db")
    c = conn.cursor()
    x = [row for row in c.execute(kentucky)]
    assert len(x) == 6


def test_dynamo_kentucky(k_crit: List[float]):
    qu = Criteria(
        k_crit[DLoad.latMax],
        k_crit[DLoad.latMin],
        k_crit[DLoad.lonMin],
        k_crit[DLoad.lonMax],
    )
    qu.query(BboxSides)
    print(qu.reduce())


@pytest.mark.skip
def test_low_level(k_crit):
    conn = Connection()
    condition = NumberAttribute(attr_name="lat_u") <= k_crit[DLoad.latMax]
    resp = [
        x["ids"]["S"]
        for x in conn.rate_limited_scan(
            "BboxSides",
            filter_condition=condition,
            attributes_to_get=["ids"],
            index_name="lat-u-index",
        )
    ]
    for r in resp:
        print(sorted(r))
