import os
from dotenv import load_dotenv
from bot import MinecraftServerBot

if __name__ == "__main__":
    # * Load environment variable
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    minecraft_api_root = os.getenv("MINECRAFT_API_PATH")

    # * run bot
    bot = MinecraftServerBot(minecraft_api_root)
    bot.run(token=token)
