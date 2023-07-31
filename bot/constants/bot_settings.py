from envparse import Env

env = Env()

BOT_TOKEN = env.str("TG_BOT_TOKEN")
API_KEY = env.str("API_KEY")
BOT_DEBUG = env.bool("BOT_DEBUG", default=False)


# webhook settings
WEBHOOK_PATH = "/"
WEBHOOK_URL = "https://drivex.fun/bot"


# webserver settings
WEBAPP_PORT = 8888
WEBAPP_HOST = env.str("WEBAPP_HOST")


CHANNEL_ID = "@InterCity_app"
ADMIN_ID = 1338248618
