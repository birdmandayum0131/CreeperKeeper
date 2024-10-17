import os
import aiohttp
import discord
import button
import asyncio
import data.message


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

    def __init__(self):
        super().__init__(timeout=None)
        self.api_root = os.getenv("MINECRAFT_API_PATH")
        self.start_server_endpoint = self.api_root + "/api/v1/server/minecraft/start"
        self.stop_server_endpoint = self.api_root + "/api/v1/server/minecraft/stop"
        self.server_status_endpoint = self.api_root + "/api/v1/server/minecraft/status"

        self.start_button = button.StartServerButton()
        self.stop_button = button.StopServerButton()
        self.refresh_button = button.RefreshServerButton()

        self.start_button.callback = self.startServerCallback
        self.stop_button.callback = self.stopServerCallback
        self.refresh_button.callback = self.refreshButtonCallback

        self.add_item(self.start_button)
        self.add_item(self.stop_button)
        self.add_item(self.refresh_button)

    async def startServerCallback(self, interaction: discord.Interaction):
        # * refresh view before any server action
        await self.RefreshServerStatus()
        if self._error is not None:
            await interaction.response.edit_message(content=self.ServerControlMessage, view=self)
            return

        err, _ = await self.request2MCServer("Start Server")
        if err is not None:
            print("Start server failed:" + err)
            self._error = err
            await interaction.response.edit_message(content=self.ServerControlMessage, view=self)
            return

        self._serverStatus = "pending"
        self.updateView()
        await interaction.response.edit_message(content=self.ServerControlMessage, view=self)
        await asyncio.sleep(60)

        # * refresh view after server action
        await self.RefreshServerStatus()
        await interaction.message.edit(content=self.ServerControlMessage, view=self)

    async def stopServerCallback(self, interaction: discord.Interaction):
        # * refresh view before any server action
        await self.RefreshServerStatus()
        if self._error is not None:
            await interaction.response.edit_message(content=self.ServerControlMessage, view=self)
            return

        err, _ = await self.request2MCServer("Stop Server")
        if err is not None:
            print("Stop server failed:" + err)
            self._error = err
            await interaction.response.edit_message(content=self.ServerControlMessage, view=self)
            return

        self._serverStatus = "pending"
        self.updateView()
        await interaction.response.edit_message(content=self.ServerControlMessage, view=self)
        await asyncio.sleep(60)

        # * refresh view after server action
        await self.RefreshServerStatus()
        await interaction.message.edit(content=self.ServerControlMessage, view=self)

    async def refreshButtonCallback(self, interaction: discord.Interaction):
        """Fetch the server status and update the view."""
        await self.RefreshServerStatus()
        await interaction.response.edit_message(content=self.ServerControlMessage, view=self)

    async def RefreshServerStatus(self):
        """Fetch the server status and update the view state."""
        err, data = await self.request2MCServer("Fetch Status")
        if err is not None:
            print("Fetch server status failed:" + err)
            self._serverStatus = "unknown"
            self._error = err
            self.updateView()  # * udpate view before edit message
            return

        self._serverStatus = data.get("serverStatus")
        self._error = None
        self.updateView()  # * udpate view before edit message

    def updateView(self):
        """Update view items with server status.

        Args:
            server_status (str): The status of the server, fetched from minecraft api.
        """
        match self._serverStatus:
            case "online":
                self.start_button.disabled = True
                self.stop_button.disabled = False
            case "offline":
                self.start_button.disabled = False
                self.stop_button.disabled = True
            case _:
                self.start_button.disabled = True
                self.stop_button.disabled = True

    async def request2MCServer(self, action: str) -> tuple[str | None, dict | None]:
        """Define how to request to minecraft api for each action.

        Args:
            action (str): enum["Start Server", "Stop Server", "Fetch Status"]

        Raises:
            ValueError: raise when action | requestType is not defined.

        Returns:
            tuple[str | None, dict | None]: (err, data)
        """
        match action:
            case "Start Server":
                endpoint = self.start_server_endpoint
                requestType = "POST"
            case "Stop Server":
                endpoint = self.stop_server_endpoint
                requestType = "POST"
            case "Fetch Status":
                endpoint = self.server_status_endpoint
                requestType = "GET"
            case _:
                raise ValueError(f"Invalid action: {action}")
        async with aiohttp.ClientSession() as session:
            match requestType:
                case "POST":
                    async with session.post(endpoint) as resp:
                        if resp.status != 200:
                            return await resp.text(), None
                        return None, await resp.json()
                case "GET":
                    async with session.get(endpoint) as resp:
                        if resp.status != 200:
                            return await resp.text(), None
                        return None, await resp.json()
                case _:
                    raise ValueError(f"Undefined request type: {requestType}")

    @property
    def ServerControlMessage(self) -> str:
        error_message = data.message.Error(self._error) if self._error is not None else ""
        return data.message.minecraft_server_message.format(serverStatus=self._serverStatus, errorMessage=error_message)
