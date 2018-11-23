import click

from dynageo.dynageo import dbInit, dbLoad

@click.group()
def main():
    """Main interface
    """
    pass


@main.command()
def dbInit():
    """Initialize the stagging db to hold shapefile data
    """
    pass


@main.command()
def dbLoad():
    """Read shapefile data into staging db.
    """
    pass


@main.command()
def dyInit():
    """Initialize the dynamodb table
    """
    pass


@main.command()
def dyLoad():
    """Load dynamodb table from the staging db table.
    """
    pass


@main.command()
def dyQuery():
    """Run a query against dynamodb
    """
    pass
