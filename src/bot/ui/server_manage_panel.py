from typing import Callable

from discord import Interaction

from domain import ServerStatus

from .server_manage_button import RefreshServerButton, StartServerButton, StopServerButton


class ServerManagePanel:
    """A UI class that define all server control buttons

    This class define pure UI logic, without server control logic.
    This is just a helper class for ServerManageView, so it doesn't need to inherit from discord.ui.View.

    Attributes:
        start_button (discord.ui.Button): The button for starting the server.
        stop_button (discord.ui.Button): The button for stopping the server.
        refresh_button (discord.ui.Button): The button for fetching the server status.
    """

    def __init__(
        self,
        start_server_callback: Callable[[Interaction], None],
        stop_server_callback: Callable[[Interaction], None],
        refresh_status_callback: Callable[[Interaction], None],
        id_prefix: str = "",
    ):
        self.start_server_button = StartServerButton(id_prefix)
        self.stop_server_button = StopServerButton(id_prefix)
        self.refresh_status_button = RefreshServerButton(id_prefix)

        self.start_server_button.callback = start_server_callback
        self.stop_server_button.callback = stop_server_callback
        self.refresh_status_button.callback = refresh_status_callback

    def __iter__(self):
        return iter([self.start_server_button, self.stop_server_button, self.refresh_status_button])

    def update_pannel(self, server_status: ServerStatus):
        """Update the panel with the current server status.

        Args:
            server_status (ServerStatus): The current server status.
        """
        self.start_server_button.disabled = server_status != ServerStatus.OFFLINE
        self.stop_server_button.disabled = server_status != ServerStatus.ONLINE
        self.refresh_status_button.disabled = server_status == ServerStatus.STARTING or server_status == ServerStatus.STOPPING
