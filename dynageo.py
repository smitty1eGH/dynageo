import click

from dynageo.dynageo import dbInit, dbLoad


@click.group()
def main():
    """Main interface
    """
    pass


@main.command()
def databaseInit():
    """Initialize the stagging db to hold shapefile data
    """
    dbInit()

@main.command()
def databaseLoad():
    """Read shapefile data into staging db.
    """
    dbLoad()


@main.command()
def dynamoInit():
    """Initialize the dynamodb table
    """
    pass


@main.command()
def dynamoLoad():
    """Load dynamodb table from the staging db table.
    """
    pass


@main.command()
def dyQuery():
    """Run a query against dynamodb
    """
    pass
