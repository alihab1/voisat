import os

class Config(object):
    # Token Bot
    TG_BOT_TOKEN = TeleBot("TG_BOT_TOKEN")
    API_ID = int(os.environ.get("API_ID"))
           ID = int(os.environ.get("ID"))
    API_HASH = os.environ.get("API_HASH")
