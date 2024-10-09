import discord


class StartServerButton(discord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(label="Start Minecraft Server", style=discord.ButtonStyle.green, disabled=disabled)


class StopServerButton(discord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(label="Stop Minecraft Server", style=discord.ButtonStyle.grey, disabled=disabled)
