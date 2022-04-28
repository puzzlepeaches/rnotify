from watchfiles import watch
from pathlib import Path


class File:
    """Watch for file changes"""

    def __init__(self, target, notify_handler, notifier, notify, filter):
        self.target = target
        self.notify_handler = notify_handler
        self.notifier = notifier
        self.notify = notify
        self.filter = filter

    def observer(self):

        # Setting up and starting file watcher

        # Predefining messages
        messages = []

        # Watching target
        for changes in watch(self.target):
            for change in changes:

                # Getting latest change
                with open(self.target, "r") as f:
                    last_line = f.readlines()[-1]

                # Getting filename
                path = Path(self.target)

                # If filter is defined search for it in latest line
                if self.filter:
                    if self.filter in last_line:
                        messages.append(f"File changed: {path.name}")
                        messages.append(f"Last line: {last_line}")
                        for m in messages:
                            self.notify.notified(
                                m, self.notify_handler, self.notifier)
                        messages = []
                    else:
                        pass

                # If filter not defined, just notify on change
                else:
                    messages.append(f"File changed: {path.name}")
                    messages.append(f"Last line: {last_line}")
                    for m in messages:
                        self.notify.notified(
                            m, self.notify_handler, self.notifier)
                    messages = []
