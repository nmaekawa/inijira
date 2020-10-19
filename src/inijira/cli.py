# -*- coding: utf-8 -*-

"""Console script for hxann."""
import contextlib
import sys
import click

from dotenv import load_dotenv
import os

from inijira.inijira import convert


# if dotenv file, load it
dotenv_path = os.environ.get("INIJIRA_DOTENV_PATH", None)
if dotenv_path:
    # BEWARE that dotenv overrides what's already in env
    load_dotenv(dotenv_path, override=True)


@click.command()
@click.option(
    "--doc",
    default="-",
    help="confluence html export file path",
)
def cli(doc):
    with _smart_open(doc) as handle:
        content = handle.read()

    result = convert(content)
    click.echo(result)


# from http://stackoverflow.com/a/29824059
@contextlib.contextmanager
def _smart_open(filename, mode="Ur"):
    if filename == "-":
        if mode is None or mode == "" or "r" in mode:
            fhandle = sys.stdin
        else:
            fhandle = sys.stdout
    else:
        fhandle = open(filename, mode)

    try:
        yield fhandle
    finally:
        if filename != "-":
            fhandle.close()


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
