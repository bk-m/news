# -*- coding: utf-8 -*-

"""Console script for news."""

import click


@click.command()
def main(args=None):
    """Console script for news."""
    click.echo("Replace this message by putting your code into "
               "news.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


if __name__ == "__main__":
    main()
