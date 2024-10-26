import aiohttp
from .server_status import ServerStatus


class MinecraftServerManager:
    """A class for managing the minecraft server."""

    def __init__(self, api_root: str, environment: str = "dev"):
        self.environment = environment
        self.start_server_endpoint = api_root + "/api/v1/server/minecraft/start"
        self.stop_server_endpoint = api_root + "/api/v1/server/minecraft/stop"
        self.server_status_endpoint = api_root + "/api/v1/server/minecraft/status"

        self.server_status = ServerStatus.UNKNOWN
        self.start_server_error = ""
        self.stop_server_error = ""
        self.fetch_server_error = ""

    async def start_server(self) -> str:
        """Send a POST request to the Minecraft-API to start the server.

        Returns:
            str: The error message if the request is not successful, otherwise empty string.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(self.start_server_endpoint) as resp:
                if resp.status != 200:
                    self.start_server_error = await resp.text()
                else:
                    self.start_server_error = ""
                return self.start_server_error

    async def stop_server(self) -> str:
        """Send a POST request to the Minecraft-API to stop the server.

        Returns:
            str: The error message if the request is not successful, otherwise empty string.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(self.stop_server_endpoint) as resp:
                if resp.status != 200:
                    self.stop_server_error = await resp.text()
                else:
                    self.stop_server_error = ""
                return self.stop_server_error

    async def fetch_server_status(self) -> tuple[str, ServerStatus]:
        """Send a GET request to the Minecraft-API to fetch the server status.

        Returns:
            tuple[Optional[str], Optional[ServerStatus]]: A tuple of error message and server status.
                If the request is not successful, the first element is the response text, otherwise None.
                If the server status is unknown, the second element is ServerStatus.UNKNOWN, otherwise the actual server status.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.server_status_endpoint) as resp:
                if resp.status != 200:
                    self.fetch_server_error = await resp.text()
                    self.server_status = ServerStatus.UNKNOWN
                else:
                    self.fetch_server_error = ""
                    data = await resp.json()
                    status = data.get("serverStatus")
                    # iterate ServerStatus to match response
                    self.server_status = next((s for s in ServerStatus if s.value == status), ServerStatus.UNKNOWN)
                return self.fetch_server_error, self.server_status

    @property
    def error_message(self) -> str:
        return "\n".join([self.start_server_error, self.stop_server_error, self.fetch_server_error])
