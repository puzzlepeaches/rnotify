import time
import click
import click_config_file
from pathlib import Path
from notifiers import get_notifier
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class NotifyHandler(FileSystemEventHandler):
    """Custom event handler for filesystem changes"""

    def __init__(self, webhook, notifier):
        self.webhook = webhook
        self.notifier = notifier

    def on_created(self, event):
        if event.event_type == "created":
            path = Path(event.src_path)
            print(f"File created: {path.name}")
            try:
                self.notifier.notify(
                    message=f"File created: {path.name}", webhook_url=self.webhook
                )
            except Exception as e:
                print(f"Failed to notify: {e}")
                exit(1)


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


@click.command(no_args_is_help=False, context_settings=CONTEXT_SETTINGS)
@click.option("-d", "--directory", default=".", help="Directory to watch.")
@click.option("-w", "--webhook", help="Slack Webhook URL.")
@click.option("-s", "--sleep", 'interval', help="Sleep time between checks", default=5)
@click_config_file.configuration_option()
def main(directory, webhook, interval):
    """Notify on new files in a directory"""

    # Getting slack notifier
    notifier = get_notifier("slack")

    # Setting up event handler
    event_handler = NotifyHandler(webhook, notifier)

    # Getting observer
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    # Starting infinite loop observations
    try:
        while True:
            time.sleep(interval)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
