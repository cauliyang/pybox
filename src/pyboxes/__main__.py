"""Command-line interface."""
import os
from typing import Any
from typing import Dict

import click

plugin_folder = os.path.join(os.path.dirname(__file__), "commands")


class MyCLI(click.MultiCommand):
    """Command-line interface to integrate with more commands."""

    def list_commands(self, ctx: click.Context) -> list[str]:
        """List all available commands.

        Args:
            ctx: click.Context

        Returns: the list of commands
        """
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx: click.Context, name: str) -> Any:
        """Get the command object.

        Args:
            ctx: click.Context
            name: the name of the command

        Raises:
            UsageError: if the command is not found.

        Returns: the command object

        """
        ns: Dict[str, Any] = {}
        fn = os.path.join(plugin_folder, name + ".py")
        try:
            with open(fn) as f:
                code = compile(f.read(), fn, "exec")
                eval(code, ns, ns)
        except FileNotFoundError:
            raise click.UsageError(
                f"Command {name} not found\nTry pybox -h for help"
            ) from FileNotFoundError
        else:
            return ns["cli"]


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=150)
help_message = """This tool include a bunch of useful commands:\n
\b
1. Download single file or all files in a folder for Google Driver
2. Send message to Slack
3. more to come...
"""

main = MyCLI(
    help=help_message,
    context_settings=CONTEXT_SETTINGS,
    subcommand_metavar="<command>",
    options_metavar="[options]",
)

if __name__ == "__main__":
    main()
