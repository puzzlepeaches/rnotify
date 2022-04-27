import time
import click
import click_config_file

# from lib.pid import Pid
# from lib.file import File
from .lib.utils import *
from .lib.notify import Notify
from .lib.folder import Folder

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


@click.group()
def cli():
    """Notify on arbitrary filesystem events and process state changes."""
    pass


@cli.command(no_args_is_help=False, context_settings=CONTEXT_SETTINGS)
@click.argument("target", type=click.Path(exists=True))
@click.option("-w", "--webhook", help="Webhook URL", required=True)
@click.option(
    "-n",
    "--notifier",
    type=click.Choice(["teams", "slack", "discord"]),
    help="Notification provider.",
    required=True,
)
@click.option(
    "-s",
    "--sleep",
    "interval",
    help="Sleep time between checks",
    default=5,
    show_default=True,
)
@click_config_file.configuration_option()
def file(target, notifier, webhook, interval):
    """Notify on file changes"""

    # Validating webhook
    if validate_url(webhook):
        pass

    # Initializing notification handler
    notif_handler = Notify(webhook, notifier)


@cli.command(no_args_is_help=False, context_settings=CONTEXT_SETTINGS)
@click.argument("target", type=int)
@click.option("-w", "--webhook", help="Webhook URL", required=True)
@click.option(
    "-n",
    "--notifier",
    type=click.Choice(["teams", "slack", "discord"]),
    help="Notification provider.",
    required=True,
)
@click.option(
    "-s",
    "--sleep",
    "interval",
    help="Sleep time between checks",
    default=5,
    show_default=True,
)
@click_config_file.configuration_option()
def pid(target, notifier, webhook, interval):
    """Notify on process changes"""

    # Validating webhook
    if validate_url(webhook):
        pass

    # Initializing notification handler
    notif_handler = Notify(webhook, notifier)


@cli.command(no_args_is_help=False, context_settings=CONTEXT_SETTINGS)
@click.argument("target", type=click.Path(exists=True))
@click.option("-w", "--webhook", help="Webhook URL", required=True)
@click.option("-d", "--daemon", help="Daemonize", is_flag=True)
@click.option(
    "-n",
    "--notifier",
    type=click.Choice(["teams", "slack", "discord"]),
    help="Notification provider.",
    required=True,
)
@click.option(
    "-s",
    "--sleep",
    "interval",
    help="Sleep time between checks",
    default=5,
    show_default=True,
)
@click_config_file.configuration_option()
def folder(target, notifier, webhook, daemon, interval):
    """Notify on directory changes"""

    # Validating webhook
    if validate_url(webhook):
        pass

    # Initializing notification handler
    notify = Notify(webhook, notifier)
    notify_handler = notify.init_notifier()

    # Initializing folder watcher
    watch = Folder(target, notify_handler, interval, webhook)
    observer = watch.observer()
    observer.start()

    # Daemonize if set
    if daemon:
        ts = int(time.time())
        pidfile = f"/tmp/{ts}.folder.notify.pid"
        daemonized = Daemonized(pidfile)
        daemonized.start()

    try:
        while True:
            time.sleep(interval)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    cli()
