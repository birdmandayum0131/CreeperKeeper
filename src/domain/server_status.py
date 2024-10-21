from enum import StrEnum


class ServerStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    PENDING = "pending"
    UNKNOWN = "unknown"
