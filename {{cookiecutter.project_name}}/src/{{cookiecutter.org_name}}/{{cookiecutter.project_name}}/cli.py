#!/usr/bin/env python3
# vim: set filetype=python sts=4 ts=4 sw=4 expandtab tw=88 cc=+1:
# vim: set filetype=python tw=88 cc=+1:

import logging
import os
import sys
import typing

import typer

LOGGER = logging.getLogger(__name__)

"""
https://click.palletsprojects.com/en/7.x/api/#parameters
https://click.palletsprojects.com/en/7.x/options/
https://click.palletsprojects.com/en/7.x/arguments/
https://typer.tiangolo.com/
https://typer.tiangolo.com/tutorial/options/
"""


cli = typer.Typer()
cli_sub = typer.Typer()
cli.add_typer(cli_sub, name="sub")


@cli.callback()
def cli_callback(
    ctx: typer.Context, verbosity: int = typer.Option(0, "--verbose", "-v", count=True)
) -> None:
    if verbosity is not None:
        root_logger = logging.getLogger("")
        root_logger.propagate = True
        new_level = (
            root_logger.getEffectiveLevel()
            - (min(1, verbosity)) * 10
            - min(max(0, verbosity - 1), 9) * 1
        )
        root_logger.setLevel(new_level)

    LOGGER.debug(
        "entry: ctx.parent.params = %s, ctx.params = %s",
        ({} if ctx.parent is None else ctx.parent.params),
        ctx.params,
    )
    LOGGER.debug(
        "logging.level = %s, LOGGER.level = %s",
        logging.getLogger("").getEffectiveLevel(),
        LOGGER.getEffectiveLevel(),
    )


@cli_sub.callback()
def cli_sub_callback(ctx: typer.Context) -> None:

    LOGGER.debug(
        "entry: ctx.parent.params = %s, ctx.params = %s",
        ({} if ctx.parent is None else ctx.parent.params),
        ctx.params,
    )


@cli_sub.command("leaf")
def cli_sub_leaf(
    ctx: typer.Context,
    name: typing.Optional[str] = typer.Option(
        "fake", "--name", "-n", help="The name ..."
    ),
    numbers: typing.Optional[typing.List[int]] = typer.Argument(None),
) -> None:

    LOGGER.debug(
        "entry: ctx.parent.params = %s, ctx.params = %s",
        ({} if ctx.parent is None else ctx.parent.params),
        ctx.params,
    )


def main() -> None:
    logging.basicConfig(
        level=os.environ.get("PYLOGGING_LEVEL", logging.INFO),
        stream=sys.stderr,
        datefmt="%Y-%m-%dT%H:%M:%S",
        format=(
            "%(asctime)s %(process)d %(thread)d %(levelno)03d:%(levelname)-8s "
            "%(name)-12s %(module)s:%(lineno)s:%(funcName)s %(message)s"
        ),
    )

    cli()


if __name__ == "__main__":
    main()
