import discord


class StartServerButton(discord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(
            label="Start Minecraft Server",
            style=discord.ButtonStyle.green,
            disabled=disabled,
            custom_id="start_server_button",
        )


class StopServerButton(discord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(
            label="Stop Minecraft Server",
            style=discord.ButtonStyle.grey,
            disabled=disabled,
            custom_id="stop_server_button",
        )


class RefreshServerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Refresh Server Status",
            style=discord.ButtonStyle.blurple,
            custom_id="refresh_status_button",
        )
