import os
import aiohttp
import discord
import button
import asyncio
from data.message import minecraft_server_message


class ServerManageView(discord.ui.View):
    def __init__(self, server_status: str = "offline"):
        super().__init__(timeout=None)
        self.api_root = os.getenv("MINECRAFT_API_PATH")
        self.startButton = button.StartServerButton(disabled=True)
        self.stopButton = button.StopServerButton(disabled=True)
        self.serverOnline = server_status == "online"
        self.startButton.callback = self.startServerCallback
        self.stopButton.callback = self.stopServerCallback
        self.startButton.disabled = self.serverOnline
        self.stopButton.disabled = not self.serverOnline

        self.add_item(self.startButton)
        self.add_item(self.stopButton)

    async def startServerCallback(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.post(os.getenv("MINECRAFT_API_PATH") + "/api/v1/server/minecraft/start") as resp:
                if resp.status != 200:
                    err = await resp.text()
                    interaction.response.send_message("Error: " + err)
                    return

        self.startButton.disabled = True
        await interaction.response.edit_message(view=self)
        await asyncio.sleep(60)
        self.stopButton.disabled = False
        await interaction.message.edit(content=minecraft_server_message.format(serverStatus="online"), view=self)

    async def stopServerCallback(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.post(os.getenv("MINECRAFT_API_PATH") + "/api/v1/server/minecraft/stop") as resp:
                if resp.status != 200:
                    err = await resp.text()
                    interaction.response.send_message("Error: " + err)
                    return

        self.stopButton.disabled = True
        await interaction.response.edit_message(view=self)
        await asyncio.sleep(60)
        self.startButton.disabled = False
        await interaction.message.edit(content=minecraft_server_message.format(serverStatus="offline"), view=self)
