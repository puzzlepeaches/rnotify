import os
import time
import click
import daemon
import psutil
import click_config_file

from .lib.pid import Pid
from .lib.file import File
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
@click.option("-f", "--filter", help="Filter changes by string.", required=False)
@click.option(
    "-s",
    "--sleep",
    "interval",
    help="Sleep time between checks",
    default=5,
    show_default=True,
)
@click.option(
    "-d", "--daemon", "create_daemon", help="Daemonize the utility", is_flag=True
)
@click_config_file.configuration_option()
def file(target, notifier, webhook, create_daemon, interval, filter):
    """Notify on file changes"""

    # Validating webhook
    validate_url(webhook)

    # Initializing notification handler
    notify = Notify(webhook, notifier)
    notify_handler = notify.init_notifier()

    # Initializing file watcher
    watch = File(target, notify_handler, notifier, notify, filter)

    # Daemonize if set
    if create_daemon:
        with daemon.DaemonContext(detach_process=True):
            while True:
                try:
                    watch.observer()
                    time.sleep(interval)
                except KeyboardInterrupt:
                    exit(1)
    else:
        try:
            watch.observer()
            time.sleep(interval)
        except KeyboardInterrupt:
            exit(1)


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
@click.option(
    "-d", "--daemon", "create_daemon", help="Daemonize the utility", is_flag=True
)
@click_config_file.configuration_option()
def pid(target, notifier, webhook, create_daemon, interval):
    """Notify on process changes"""

    # Validating webhook
    validate_url(webhook)

    # Initializing notification handler
    notify = Notify(webhook, notifier)
    notify_handler = notify.init_notifier()

    # Initializing PID tracker
    pid = Pid(target, notify_handler, notifier, notify)

    # Making sure process exists already
    if pid.observer():
        pass
    else:
        click.echo(f"Process {target} does not exist.")
        exit(1)

    # Daemonize if set
    if create_daemon:
        with daemon.DaemonContext(detach_process=True):
            while True:
                try:
                    status = pid.observer()
                    if not status:
                        message = f"Process {target} has stopped running."
                        notify.notified(message, notify_handler, notifier)
                        exit(0)
                    else:
                        continue
                    time.sleep(interval)
                except KeyboardInterrupt:
                    exit(1)
    else:
        while True:
            try:
                status = pid.observer()
                if not status:
                    message = f"Process {target} has stopped running."
                    notify.notified(message, notify_handler, notifier)
                    exit(0)
                else:
                    continue
                time.sleep(interval)
            except KeyboardInterrupt:
                exit(1)


@cli.command(no_args_is_help=False, context_settings=CONTEXT_SETTINGS)
@click.argument("target", type=click.Path(exists=True))
@click.option("-w", "--webhook", help="Webhook URL", required=True)
@click.option(
    "-d", "--daemon", "create_daemon", help="Daemonize the utility", is_flag=True
)
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
def folder(target, notifier, webhook, create_daemon, interval):
    """Notify on directory changes"""

    # Validating webhook
    validate_url(webhook)

    # Initializing notification handler
    notify = Notify(webhook, notifier)
    notify_handler = notify.init_notifier()

    # Initializing folder watcher
    watch = Folder(target, notify_handler, notifier, notify)
    observer = watch.observer()
    observer.start()

    # Daemonize if set
    if create_daemon:
        with daemon.DaemonContext(detach_process=True):
            while True:
                try:
                    time.sleep(interval)
                except KeyboardInterrupt:
                    observer.stop()
                    exit(1)
                observer.join()
    else:
        try:
            while True:
                time.sleep(interval)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    cli()
