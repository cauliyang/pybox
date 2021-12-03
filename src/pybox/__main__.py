"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Pybox."""


if __name__ == "__main__":
    main(prog_name="pybox")  # pragma: no cover
