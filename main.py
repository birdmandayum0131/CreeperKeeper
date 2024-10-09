import os
import commands  # * setup commands
from dotenv import load_dotenv
from client import defaultClient as bot

# * Load environment variable
load_dotenv()
token = os.getenv("BOT_TOKEN")

# * run bot
bot.run(token=token)
