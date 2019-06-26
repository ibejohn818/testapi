# -*- coding: utf-8 -*-

"""Console script for mtaws."""
import sys
import click
from mtaws import __version__ as version


@click.command()
def main(args=None):
    print("VERSION: ", version)
    pass



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
