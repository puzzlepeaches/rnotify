from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Folder(FileSystemEventHandler):
    
    def __init__(self, target, notify_handler, interval):
        self.target = target
        self.notify_handler = notify_handler
        self.interval = interval

    def observer(self):
        observer = Observer()
        observer.schedule(self, self.target, recursive=False)
        observer.start()
        return observer
    
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


