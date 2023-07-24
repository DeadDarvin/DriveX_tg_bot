from envparse import Env

env = Env()

BOT_TOKEN = env.str("TG_BOT_TOKEN", default="5527908760:AAG3wQicZhI_suBJVyrosjCA0SCzXmiSrUo")

WEBHOOK_HOST = "https://test"
WEBHOOK_PATH = '/bot'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8000

BOT_DEBUG = env.bool("BOT_DEBUG", default=True)
