import discord
from discord.ext import commands

# * Create default client
intents = discord.Intents.default()
intents.message_content = True
defaultClient = commands.Bot(command_prefix='!', intents=intents)
