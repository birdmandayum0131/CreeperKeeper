import discord
from discord.ext import commands

from domain import MinecraftServerManager

from .cogs import Minecraft
from .ui import ServerManageView


class MinecraftServerBot(commands.Bot):
    def __init__(self, api_root: str):
        self.api_root = api_root
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    async def setup_hook(self) -> None:
        self.server_manager = MinecraftServerManager(self.api_root)
        self.server_manage_view = ServerManageView(self.server_manager)
        await self.add_cog(Minecraft(self, self.server_manage_view))
        self.add_view(ServerManageView(self.server_manager))
