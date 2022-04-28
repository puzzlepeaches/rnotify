from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Folder(FileSystemEventHandler):
    """Monitors for additions to target directory"""

    def __init__(self, target, notify_handler, notifier, notify):
        self.target = target
        self.notify_handler = notify_handler
        self.notifier = notifier
        self.notify = notify

    def observer(self):
        """Using watchdog library to make observations"""
        observer = Observer()
        observer.schedule(self, self.target, recursive=False)
        return observer

    def on_created(self, event):
        """If a file is created, trigger a notification"""
        if event.event_type == "created":
            path = Path(event.src_path)
            message = f"File created: {path.name}"
            self.notify.notified(message, self.notify_handler, self.notifier)
