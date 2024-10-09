from typing import Union
from data.message import chaos_message
from client import defaultClient as bot
from discord import Reaction, Member, User


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
