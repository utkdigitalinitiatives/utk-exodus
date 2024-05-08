#!/usr/bin/env python3

from utk_exodus.finder import FileOrganizer
from utk_exodus.curate import FileCurator
from utk_exodus.metadata import MetadataMapping
from utk_exodus.validate import ValidateMigration
from utk_exodus.controller import InterfaceController
import click
import os
import requests


@click.group()
def cli() -> None:
    pass


@cli.command("works", help="Create import sheet for works with metadata.")
@click.option(
    "--config",
    "-c",
    default="data/utk_dc.yml",
    help="Path to the configuration file for metadata mapping.",
)
@click.option(
    "--path",
    "-p",
    required=True,
    help="Path to the directory containing the metadata files.",
)
@click.option(
    "--output",
    "-o",
    default="delete/works.csv",
    help="Path to the output file you want to write to.",
)
def works(config: str, path: str, output: str) -> None:
    metadata = MetadataMapping(config, path)
    metadata.write_csv(output)
    r = requests.get(
        "https://raw.githubusercontent.com/utkdigitalinitiatives/m3_profiles/main/maps/utk.yml"
    )
    with open("delete/m3.yml", "wb") as f:
        f.write(r.content)
    print("Validating import ...")
    validator = ValidateMigration(profile="delete/m3.yml", migration_sheet=output)
    validator.iterate()


@cli.command(
    "add_files", help="Add filesets and attachments to and existing import sheet."
)
@click.option(
    "--sheet", "-s", help="Specify the original metadata works csv.", required=True
)
@click.option("--files_sheet", "-f", help="Optional: specify new sheet to write to.")
@click.option(
    "--what_to_add",
    "-w",
    help="Specify adding attachments, filesheets, or everything",
    default="everything",
)
@click.option(
    "--remote",
    "-r",
    help="Specify remote address of files",
    default="https://digital.lib.utk.edu/collections/islandora/object/",
)
def add_files(sheet: str, files_sheet: str, what_to_add: str, remote: str) -> None:
    if not files_sheet:
        files_sheet = f"{sheet.replace('.csv', '')}_with_filesets_and_attachments.csv"
    if what_to_add == "everything":
        what_to_add = ["filesets", "attachments"]
    """Take a CSV and Add files to it"""
    x = FileOrganizer(sheet, what_to_add, remote)
    x.write_csv(files_sheet)


@cli.command("works_and_files", help="Create import sheet with works and files.")
@click.option(
    "--config",
    "-c",
    default="data/utk_dc.yml",
    help="Path to the configuration file for metadata mapping.",
)
@click.option(
    "--collection",
    "-l",
    help="Specify the collection you want to download metadata for."
)
@click.option(
    "--model",
    "-m",
    type=click.Choice(
        ['book', 'image', 'pdf', 'audio', 'video'],
        case_sensitive=False
    ),
    help="The model you want to download metadata for."
)
@click.option(
    "--path",
    "-p",
    help="Path to the directory containing the metadata files.",
)
@click.option(
    "--output",
    "-o",
    default="new_set",
    help="Path to the output directory you want to create.",
)
@click.option(
    "--remote",
    "-r",
    help="Specify remote address of files",
    default="https://digital.lib.utk.edu/collections/islandora/object/",
)
@click.option(
    "--total_size",
    "-t",
    help="Specify maximum number of attachments and filesets per sheet.",
    default=800,
)
def works_and_files(
        collection: str,
        config: str,
        model: str,
        path: str,
        output: str,
        remote: str,
        total_size: int
) -> None:
    if model and collection:
        interface = InterfaceController(config, output, remote, total_size)
        interface.download_mods(collection, model)
    elif path:
        interface = InterfaceController(config, output, remote, total_size)
        interface.build_import_from_directory(path)
    else:
        print("You must specify either a path to a directory or both a collection and model.")
