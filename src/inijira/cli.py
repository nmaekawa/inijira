# -*- coding: utf-8 -*-

"""Console script for hxann."""
import contextlib
import os
import sys

import click
from dotenv import load_dotenv

from inijira.inijira import tocsv, toticket

# if dotenv file, load it
dotenv_path = os.environ.get("INIJIRA_DOTENV_PATH", None)
if dotenv_path:
    # BEWARE that dotenv overrides what's already in env
    load_dotenv(dotenv_path, override=True)


@click.command()
@click.option(
    "--doc",
    default="-",
    help="confluence html export file path, mutually exclusive from --docdir",
)
@click.option(
    "--docdir",
    help="folder with confluence html export files, mutually exclusive from --doc",
)
def cli(doc, docdir=None):
    result = []
    if docdir:
        if os.path.isdir(docdir):
            files = os.listdir(docdir)

            for f in files:
                path = os.path.join(docdir, f)
                if os.path.isfile(path):
                    row = process_single_doc(path)
                    if row:
                        result.append(row)
                else:
                    click.echo("NOT a file? {}".format(path))
        else:
            print_error("arg docdir({}) is not a dir!".format(docdir))
            exit(1)
    else:
        row = process_single_doc(doc)
        result.append(row)

    # sort result by description
    ordered = sorted(result, key=lambda x: x.get("description", "00 00 00"))
    for item in ordered:
        if item:
            """
            click.echo("{} *** {}".format(
                item.get("who", "...."),
                item.get("description", "----"),
                item.get("assignee", "++++"),
                item.get("component", "----"),
            ))
            """

    line_list = tocsv(ordered, ",")
    click.echo(line_list)


def process_single_doc(doc_path):
    with _smart_open(doc_path) as handle:
        content = handle.read()
    result = toticket(content)
    return result


def print_error(msg=""):
    click.echo("ERROR: {}".format(msg))


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
