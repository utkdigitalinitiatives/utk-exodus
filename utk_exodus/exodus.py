#!/usr/bin/env python3

from utk_exodus.finder import FileOrganizer
from utk_exodus.metadata import MetadataMapping
from utk_exodus.validate import ValidateMigration
from utk_exodus.controller import InterfaceController
from utk_exodus.template import ImportTemplate
from utk_exodus.combine import ImportRefactor
from utk_exodus.checksum import HashSheet
from utk_exodus.collection import CollectionImporter
from utk_exodus.risearch import ResourceIndexSearch
import click
import requests


@click.group()
def cli() -> None:
    pass


@cli.command("works", help="Create import sheet for works with metadata.")
@click.option(
    "--config",
    "-c",
    default="config/utk_dc.yml",
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
    default="utk_dc",
    type=click.Choice(
        ["utk_dc", "samvera", "utk_dc_no_uris", "utk_dc_no_uris_or_names"],
        case_sensitive=False,
    ),
    help="The configuration you want to use. By default, utk_dc.",
)
@click.option(
    "--collection",
    "-l",
    help="Specify the collection you want to download metadata for.",
)
@click.option(
    "--model",
    "-m",
    type=click.Choice(
        ["book", "image", "large_image", "pdf", "audio", "video"], case_sensitive=False
    ),
    help="The model you want to download metadata for.",
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
    total_size: int,
) -> None:
    if model and collection:
        interface = InterfaceController(config, output, remote, total_size)
        interface.download_mods(collection, model)
    elif path:
        interface = InterfaceController(config, output, remote, total_size)
        interface.build_import_from_directory(path)
    else:
        print(
            "You must specify either a path to a directory or both a collection and model."
        )


@cli.command(
    "generate_sheet", help="Create full sample for content model from m3 profile."
)
@click.option(
    "--model",
    "-m",
    type=click.Choice(
        [
            "Attachment",
            "Audio",
            "Book",
            "CompoundObject",
            "GenericWork",
            "Image",
            "Newspaper",
            "PDF",
            "Video",
        ],
        case_sensitive=True,
    ),
    help="The content models to find rules about.",
)
@click.option(
    "--output",
    "-o",
    help="Specify where to write your output file.",
)
def generate_sheet(
    model: str,
    output: str,
) -> None:
    r = requests.get(
        "https://raw.githubusercontent.com/utkdigitalinitiatives/m3_profiles/main/maps/utk.yml"
    )
    with open("tmp/m3.yml", "wb") as f:
        f.write(r.content)
    it = ImportTemplate("tmp/m3.yml", model)
    it.write(output)


@cli.command(
    "remove_old_values", help="Remove old values from a previous import sheet."
)
@click.option(
    "--sheet",
    "-s",
    required=True,
    help="Specify the current sheet.",
)
@click.option(
    "--old_sheet",
    "-o",
    required=True,
    help="Specify the old sheet with unused values you want to remove.",
)
@click.option(
    "--new_sheet",
    "-n",
    required=True,
    help="Specify where you want to write the new sheet.",
)
def remove_old_values(
    sheet: str,
    old_sheet: str,
    new_sheet: str,
) -> None:
    ir = ImportRefactor(sheet, old_sheet)
    ir.create_csv_with_fields_to_nuke(sheet, new_sheet)
    print(f"Refactored sheet written to {new_sheet}.")


@cli.command(
    "hash_errors",
    help="Create sheet from a directory of errored import sheets.",
)
@click.option(
    "--path",
    "-p",
    required=True,
    help="Specify the path to the directory of sheets.",
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="Specify where you want to write your sheets.",
)
def hash_errors(
    path: str,
    output: str,
) -> None:
    print(f"Generating checksums for bad files in csvs in {path}.")
    hs = HashSheet(path, output)
    hs.write()
    print(f"Hash sheet written to {output}.")


@cli.command(
    "generate_collection_metadata",
    help="Generate metadata for a collection.",
)
@click.option(
    "--collection",
    "-l",
    required=False,
    help="Specify the collection you want to download metadata for.",
)
@click.option(
    "--output",
    "-o",
    required=False,
    default="tmp/collections.csv",
    help="Specify where to write output.",
)
def generate_collection_metadata(
    collection: str,
    output: str,
) -> None:
    if collection:
        print(f"Generating metadata for {collection}.")
        x = CollectionImporter([collection])
    else:
        print("Generating metadata for all collections.")
        collections = ResourceIndexSearch().find_all_collections()
        x = CollectionImporter(collections)
    x.write_csv(output)
    print("Done. Metadata written to tmp/all_collections.csv.")
