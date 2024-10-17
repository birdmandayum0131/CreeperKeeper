# * Commands
from view import ServerControlView
from discord.ext.commands import Context
from bot import bot


@bot.command()
async def ping(ctx: Context):
    await ctx.send('pong')


@bot.command()
async def minecraft(ctx: Context):
    view = ServerControlView()
    await view.RefreshServerStatus()
    await ctx.send(content=view.ServerControlMessage, view=view)
