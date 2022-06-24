from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
USER_AGENT = env.str("USER_AGENT")
DB_URI = env.str("DB_URI")

