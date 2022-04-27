import click
import click_config_file
from lib.notify import Notify
from lib.folder import Folder
from lib.file import File 
from lib.pid import Pid 

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


@click.group()
def cli():
    """Notify on arbitrary filesystem events and process state changes."""
    pass

@cli.command(no_args_is_help=False, context_settings=CONTEXT_SETTINGS)
@click.argument("target", type=click.Path(exists=True))
@click.option(
    "-n",
    "--notifier",
    type=click.Choice(["teams", "slack", "discord"]),
    help="Notification provider.",
    required=True,
)
@click.option("-w", "--webhook", help="Webhook URL", required=True)
@click.option("-s", "--sleep", "interval", help="Sleep time between checks", default=5)
def file(target, notifier, webhook, interval):
    """Notify on file changes"""

    notif_handler = Notify(webhook, notifier)


@cli.command(no_args_is_help=False, context_settings=CONTEXT_SETTINGS)
@click.argument("target")
@click.option(
    "-n",
    "--notifier",
    type=click.Choice(["teams", "slack", "discord"]),
    help="Notification provider.",
    required=True,
)
@click.option("-w", "--webhook", help="Webhook URL", required=True)
@click.option("-s", "--sleep", "interval", help="Sleep time between checks", default=5)
def pid(target, notifier, webhook, interval):
    """Notify on process changes"""

    notif_handler = Notify(webhook, notifier)


@cli.command(no_args_is_help=False, context_settings=CONTEXT_SETTINGS)
@click.argument("target", type=click.Path(exists=True))
@click.option(
    "-n",
    "--notifier",
    type=click.Choice(["teams", "slack", "discord"]),
    help="Notification provider.",
    required=True,
)
@click.option("-w", "--webhook", help="Webhook URL", required=True)
@click.option("-s", "--sleep", "interval", help="Sleep time between checks", default=5)
def folder(target, notifier, webhook, interval):
    """Notify on directory changes"""

    notif_handler = Notify(webhook, notifier)


if __name__ == "__main__":
    cli()
