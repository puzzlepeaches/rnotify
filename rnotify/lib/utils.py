import validators

def validate_url(webhook):
    if validators.url(webhook):
        pass
    else:
        raise ValueError("Invalid Webhook URL")
