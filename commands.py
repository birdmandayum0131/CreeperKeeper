# * Commands
import os
import aiohttp
from view import ServerManageView
from data.message import minecraft_server_message
from discord.ext.commands import Context
from client import defaultClient as bot


@bot.command()
async def ping(ctx: Context):
    await ctx.send('pong')


@bot.command()
async def minecraft(ctx: Context):
    async with aiohttp.ClientSession() as session:
        async with session.get(os.getenv("MINECRAFT_API_PATH") + "/api/v1/server/minecraft/status") as resp:
            if resp.status != 200:
                err = await resp.text()
                await ctx.send("Fetch server status failed:" + err)
                return

            data = await resp.json()
            minecraft_server_status = data.get("serverStatus")
            view = ServerManageView(minecraft_server_status)
            await ctx.send(content=minecraft_server_message.format(serverStatus=minecraft_server_status), view=view)