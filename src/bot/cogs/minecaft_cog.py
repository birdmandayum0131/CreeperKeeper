# * Commands
from discord.ext import commands

from ..ui import ServerManageView


class Minecraft(commands.Cog):

    # TODO: dependency on ui here is a little weird, refactor this later
    def __init__(self, bot: commands.Bot, server_manage_view: ServerManageView):
        super().__init__()
        self.bot = bot
        self.view = server_manage_view

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        print('------')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send('pong')

    @commands.command()
    async def minecraft(self, ctx: commands.Context):
        await self.view.fetch_and_update()
        await ctx.send(content=self.view.server_manage_message, view=self.view)
