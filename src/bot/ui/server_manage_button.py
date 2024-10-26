import discord


class StartServerButton(discord.ui.Button):
    def __init__(self, id_prefix: str = ""):
        super().__init__(
            label="Start Minecraft Server",
            style=discord.ButtonStyle.green,
            custom_id=id_prefix + "start_server_button",
        )


class StopServerButton(discord.ui.Button):
    def __init__(self, id_prefix: str = ""):
        super().__init__(
            label="Stop Minecraft Server",
            style=discord.ButtonStyle.grey,
            custom_id=id_prefix + "stop_server_button",
        )


class RefreshServerButton(discord.ui.Button):
    def __init__(self, id_prefix: str = ""):
        super().__init__(
            label="Refresh Server Status",
            style=discord.ButtonStyle.blurple,
            custom_id=id_prefix + "refresh_status_button",
        )
