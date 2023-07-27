from envparse import Env

env = Env()

BOT_TOKEN = env.str("TG_BOT_TOKEN")
API_KEY = env.str("API_KEY")
BOT_DEBUG = env.bool("BOT_DEBUG", default=True)


# webhook settings
WEBHOOK_PATH = "/bot"
WEBHOOK_URL = "https://drivex.fun/bot"


# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8000


# REAL_CHAT_ID =
CHAT_ID_TEST = -951650833
ADMIN_ID = 1338248618
