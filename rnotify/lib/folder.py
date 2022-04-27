from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Folder():
    def __init__(self, target, notif_handler, interval):


