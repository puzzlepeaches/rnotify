import psutil


class Pid:
    """Very simple class for now to track if pid exists"""

    def __init__(self, target, notify_handler, notifier, notify):
        self.target = target

    def observer(self):
        return psutil.pid_exists(self.target)
