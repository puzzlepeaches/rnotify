from pathlib import Path
from .notify import Notify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Folder(FileSystemEventHandler):
    def __init__(self, target, notify_handler, interval, webhook):
        self.target = target
        self.notify_handler = notify_handler
        self.interval = interval
        self.webhook = webhook

    def observer(self):
        observer = Observer()
        observer.schedule(self, self.target, recursive=False)
        return observer

    def on_created(self, event):
        if event.event_type == "created":
            path = Path(event.src_path)

            # This isn't going to work for other providers...
            self.notify_handler.notify(
                message=f"File created: {path.name}", webhook_url=self.webhook
            )
