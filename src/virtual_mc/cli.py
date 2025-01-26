"""Console script for virtual_mc."""
import virtual_mc

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for virtual_mc."""
    console.print("Replace this message by putting your code into "
               "virtual_mc.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
