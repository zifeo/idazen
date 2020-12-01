import asyncio
import json
import logging
from pathlib import Path
from typing import Optional

from bleak import BleakError
from idazen import core
import typer

cli = typer.Typer()
app_dir = Path(typer.get_app_dir("idazen"))
app_dir.mkdir(parents=True, exist_ok=True)
config_path: Path = Path(app_dir) / "config.json"
logging.debug(config_path)


def read():
    if not config_path.exists():
        return {}
    with open(config_path, "r") as f:
        return json.load(f)


def write(**kwargs):
    doc = read()
    doc.update(kwargs)
    with open(config_path, "w") as f:
        json.dump(doc, f)
    return doc


@cli.command()
def scan(duration: int = 10, save: bool = False):
    typer.echo(f"Scanning {duration}s...")
    try:
        desks = asyncio.run(core.scan(duration))
    except BleakError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1)

    if len(desks) > 1:
        typer.echo("Multiple found:")
        for name, addr in desks.items():
            typer.echo(f"  - {name} ({addr})")
        typer.echo('Use "idazen save UUID"')

    elif len(desks) == 1:
        name, addr = list(desks.items())[0]
        typer.echo(f"Found: {name} ({addr})")
        if save:
            write(desk=addr)
            typer.echo(f"Saved {name}")
        else:
            typer.echo(f'Use "idazen save {addr}" or "idazen scan --save"')

    else:
        typer.echo("None found")


@cli.command()
def save(desk: str):
    write(desk=desk)


@cli.command()
def move(height: float, desk: Optional[str] = None):

    if desk is None:
        desk = read().get("desk")

    if desk is None:
        typer.echo("Error: No desk found or specified")
        raise typer.Exit(1)

    try:
        height = asyncio.run(core.move(desk, height))
        typer.echo(f"Height set to {height}")
    except BleakError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1)


@cli.callback()
def help():
    """
    Idazen.
    """


if __name__ == "__main__":
    cli()
