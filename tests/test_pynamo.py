import inspect
import sqlite3
from typing import List

from pynamodb.attributes import NumberAttribute, UTCDateTimeAttribute
from pynamodb.expressions.condition import Comparison
import pytest

from dynageo.dynageo import BboxSides
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
    return [0.0, 39.25, 36.26, -81, 35, -89.60]


def test_sqlite_kentucky(kentucky: str):
    conn = sqlite3.connect("data/ggs650.db")
    c = conn.cursor()
    x = [row for row in c.execute(kentucky)]
    assert len(x) == 6


def test_dynamo_kentucky(k_crit: List[float]):
    condition = NumberAttribute(attr_name="lat_u") <= k_crit[DLoad.latMax]
    for z in BboxSides.lat_u_index.query("rangestamp", filter_condition=condition):
        print(z)
