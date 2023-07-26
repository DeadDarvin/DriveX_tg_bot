from envparse import Env

env = Env()

BOT_TOKEN = env.str("TG_BOT_TOKEN", default="5527908760:AAG3wQicZhI_suBJVyrosjCA0SCzXmiSrUo")
API_KEY = "75dj44brKAn96vj58hiaurfpmrCLRJDt"
BOT_DEBUG = env.bool("BOT_DEBUG", default=True)


# webhook settings
WEBHOOK_PATH = "/bot"
WEBHOOK_URL = "https://drivex.fun/bot"


# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8000


CHAT_ID_BEAR = -804109204
CHAT_ID_TEST = -951650833
