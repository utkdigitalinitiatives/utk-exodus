#!/usr/bin/env python3

from utk_exodus.metadata import MetadataMapping
import click

@click.group()
def cli() -> None:
    pass

@cli.command("works", help="Create import sheet for works with metadata.")
@click.option(
    "--config",
    "-c",
    default="data/utk_dc.yml",
)
@click.option(
    "--path",
    "-p",
    required=True,
)
@click.option(
    "--output",
    "-o",
    default="delete/works.csv"
)
def works(config: str, path: str, output: str) -> None:
    metadata = MetadataMapping(config, path)
    metadata.write_csv(output)

