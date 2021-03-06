from datetime import datetime
import sqlite3
import time

import click
import pynamodb

from data.meta import DYNOLOAD, DLoad, UBERBBOX, CONUS
from data.etl import dbInit, dbLoad
from dynageo.dynageo import BboxSides, hash_sides

LOAD_DELAY = 1


@click.group()
def main():
    """Main interface
    """
    pass


@main.command()
def databaseInit():
    """Initialize the stagging db to hold shapefile data. Will clobber
        existing data/ file.
    """
    dbInit()


@main.command()
def databaseLoad():
    """Read shapefile data into staging db.
    """
    dbLoad()
    conn = sqlite3.connect("data/ggs650.db")
    c = conn.cursor()

    print("Overall bounding box for the table:")
    [print(row) for row in c.execute(UBERBBOX)]

    print("We will limit testing to the Continental U.S.:")
    print(CONUS)
    [print(row) for row in c.execute(CONUS)]


@main.command()
def dynamoDrop():
    """Nuke the dynamodb table
    """
    if BboxSides.exists():
        BboxSides.delete_table()


@main.command()
def dynamoInit():
    """Initialize the dynamodb table
    """
    if not BboxSides.exists():
        BboxSides.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


@main.command()
def dynamoLoad():
    """Load dynamodb table from the staging db table.
    """
    conn = sqlite3.connect("data/ggs650.db")
    c = conn.cursor()
    for row in c.execute(DYNOLOAD):
        print(row)
        d = hash_sides(
            row[DLoad.latMax], row[DLoad.latMin], row[DLoad.lonMin], row[DLoad.lonMax]
        )
        e = BboxSides(
            hashkey=d,
            rangestamp=datetime.utcnow(),
            lat_u=row[DLoad.latMax],
            lat_l=row[DLoad.latMin],
            lon_w=row[DLoad.lonMin],
            lon_e=row[DLoad.lonMax],
            ids=str(row[DLoad.dist_id]),
        )
        e.save()
        time.sleep(LOAD_DELAY)


@main.command()
def dyQuery():
    """Run a query against dynamodb
    """
    pass
