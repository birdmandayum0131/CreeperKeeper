import os
import aiohttp
import discord
import button
import asyncio
from data.message import minecraft_server_message


class ServerControlView(discord.ui.View):
    """
    A view class for managing the minecraft server, with buttons of start, stop, and refresh.

    Start Button: send a POST request to minecraft api to start the server
    Stop Button: send a POST request to minecraft api to stop the server
    Refresh Button: send a GET request to minecraft api to fetch the server status

    Attributes:
        serverOnline (str): The status of the server, either "online" or "offline".
        startButton (discord.ui.Button): The button for starting the server.
        stopButton (discord.ui.Button): The button for stopping the server.
        updateButton (discord.ui.Button): The button for fetching the server status.
    """

    def __init__(self, server_status: str = "offline"):
        super().__init__(timeout=None)
        self.api_root = os.getenv("MINECRAFT_API_PATH")
        self.startButton = button.StartServerButton(disabled=True)
        self.stopButton = button.StopServerButton(disabled=True)
        self.updateButton = button.UpdateServerButton()
        self.serverOnline = server_status == "online"
        self.startButton.callback = self.startServerCallback
        self.stopButton.callback = self.stopServerCallback
        self.updateButton.callback = self.updateServerCallback
        self.startButton.disabled = self.serverOnline
        self.stopButton.disabled = not self.serverOnline

        self.add_item(self.startButton)
        self.add_item(self.stopButton)
        self.add_item(self.updateButton)

    async def startServerCallback(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.post(os.getenv("MINECRAFT_API_PATH") + "/api/v1/server/minecraft/start") as resp:
                if resp.status != 200:
                    err = await resp.text()
                    await interaction.response.send_message("Error: " + err)
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
                    await interaction.response.send_message("Error: " + err)
                    return

        self.stopButton.disabled = True
        await interaction.response.edit_message(view=self)
        await asyncio.sleep(60)
        self.startButton.disabled = False
        await interaction.message.edit(content=minecraft_server_message.format(serverStatus="offline"), view=self)

    async def updateServerCallback(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(os.getenv("MINECRAFT_API_PATH") + "/api/v1/server/minecraft/status") as resp:
                if resp.status != 200:
                    err = await resp.text()
                    await interaction.response.send_message("Error: " + err)
                    return

                data = await resp.json()
                server_status = data.get("serverStatus")
        self.serverOnline = server_status == "online"
        self.startButton.disabled = self.serverOnline
        self.stopButton.disabled = not self.serverOnline
        await interaction.response.edit_message(content=minecraft_server_message.format(serverStatus=server_status), view=self)

    @classmethod
    def ServerControlMessage(cls, server_status: str) -> str:
        return minecraft_server_message.format(serverStatus=server_status)
