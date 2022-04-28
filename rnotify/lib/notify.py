import pymsteams
from discord_webhook import DiscordWebhook
from notifiers import get_notifier


class Notify:
    """Base class for notifiers"""

    def __init__(self, webhook, notifier):
        self.webhook = webhook
        self.notifier = notifier

    def init_notifier(self):
        """Initialize notifier"""
        if self.notifier == "teams":
            handler = get_notifier(self.notifier)
            return pymsteams.connectorcard(self.webhook)
        elif self.notifier == "discord":
            handler = get_notifier(self.notifier)
            return DiscordWebhook(self.webhook)
        elif self.notifier == "slack":
            handler = get_notifier(self.notifier)
            return get_notifier("slack")
        else:
            raise Exception(f"Notifier {self.notifier} not supported")

    def notified(self, message, notify_handler, notifier):
        """Send notification"""

        if notifier == "teams":
            notify_handler.send(text=message)
        elif notifier == "discord":
            notify_handler.execute(content=message)
        elif notifier == "slack":
            notify_handler.notify(message=message, webhook_url=self.webhook)
        else:
            raise Exception(f"Notifier {notifier} not supported")
