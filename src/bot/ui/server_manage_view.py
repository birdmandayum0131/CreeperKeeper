import asyncio

import discord
from ..messages import minecraft_server_message
from .server_manage_panel import ServerManagePanel

from domain import MinecraftServerManager, ServerStatus


class ServerManageView(discord.ui.View):
    """
    A view class for managing the minecraft server, with buttons of start, stop, and refresh.

    Start Button: send a POST request to minecraft api to start the server
    Stop Button: send a POST request to minecraft api to stop the server
    Refresh Button: send a GET request to minecraft api to fetch the server status

    Attributes:
        ManagePanelHandler : A interface that define handler function for each button.
        startButton (discord.ui.Button): The button for starting the server.
        stopButton (discord.ui.Button): The button for stopping the server.
        updateButton (discord.ui.Button): The button for fetching the server status.
    """

    def __init__(self, server_manager: MinecraftServerManager):
        # * init base class with timeout None for persistent view
        super().__init__(timeout=None)
        self.server_manager = server_manager
        self.ui_panel = ServerManagePanel(
            self._start_server_callback,
            self._stop_server_callback,
            self._refresh_status_callback,
        )

        for item in self.ui_panel:
            self.add_item(item)

    async def _start_server_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        err, status = await self.fetch_and_update()
        if err or status != ServerStatus.OFFLINE:  # * can only start server if server is offline
            await interaction.message.edit(content=self.server_manage_message, view=self)
            return

        self.server_manager.server_status = ServerStatus.PENDING
        self.ui_panel.update_pannel(self.server_manager.server_status)
        await interaction.message.edit(content=self.server_manage_message, view=self)

        await self.server_manager.start_server()
        self.ui_panel.update_pannel(self.server_manager.server_status)
        await interaction.message.edit(content=self.server_manage_message, view=self)

        await asyncio.sleep(6)
        await self.fetch_and_update()
        await interaction.message.edit(content=self.server_manage_message, view=self)

    async def _stop_server_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        err, status = await self.fetch_and_update()
        if err or status != ServerStatus.ONLINE:  # * can only stop server if server is online
            await interaction.message.edit(content=self.server_manage_message, view=self)
            return

        self.server_manager.server_status = ServerStatus.PENDING
        self.ui_panel.update_pannel(self.server_manager.server_status)
        await interaction.message.edit(content=self.server_manage_message, view=self)

        await self.server_manager.stop_server()
        self.ui_panel.update_pannel(self.server_manager.server_status)
        await interaction.message.edit(content=self.server_manage_message, view=self)

        await asyncio.sleep(6)
        await self.fetch_and_update()
        await interaction.message.edit(content=self.server_manage_message, view=self)

    async def _refresh_status_callback(self, interaction: discord.Interaction):
        """Fetch the server status and update the view."""
        await self.fetch_and_update()
        await interaction.response.edit_message(content=self.server_manage_message, view=self)

    async def fetch_and_update(self) -> tuple[str, ServerStatus]:
        err, status = await self.server_manager.fetch_server_status()
        self.ui_panel.update_pannel(status)
        return err, status

    @property
    def server_manage_message(self):
        return minecraft_server_message.format(
            server_status=self.server_manager.server_status,
            error_message=self.server_manager.error_message,
        )
