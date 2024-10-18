# Creeper Keeper

A Discord bot that enables users to interact with a self-hosted Minecraft server through a server control message. Designed to enhance convenience, it simplifies server management within Discord and integrates modern DevOps practices like CI/CD and Kubernetes for scalability and ease of deployment.

Users, even those without server ownership, can easily manage the server directly from Discord, reducing the burden on the server owner when only a few players want to play. The bot relies on another repository, [Minecraft-API](), to handle server interactions via API.

## About The Project
The origin of this project stems from my experiences with friends in gaming sessions. I'm usually the one responsible for running the server, and when we're all playing together, there's no need to handle additional server access issues.  

However, after the initial excitement fades, sometimes only a few people still want to play, or our playing times become more scattered. Out of consideration to avoid bothering me, they usually won't ask me to start or stop the server just for a bit of interest.

In such cases, sharing the server files isn't an ideal solution, and hosting the server on the cloud isn't cost-effective. With a second machine available to serve as a self-hosted server, I started this project.  

**Creeper Keeper** allows non-server owners to easily control the server within the Discord environment, reducing the burden on the server owner when only a few players want to play.

## Features

The bot comes with two basic commands:

- `!ping` : Simple ping pong comamnd to check the bot's status.
- `!minecraft` : Generate a Minecraft server management message.


### Server Management Message
<img src="https://github.com/user-attachments/assets/caa109dd-45ac-4d69-ac99-8f17cca10ca9" width="600"/>

The generated management message includes:
- **Connection Info**: How to connect to the server.
- **Server Status**: Fetches and displays the current server info.
- **Management Buttons**: These buttons allow users to manage the server:
  - `Start Minecraft Server`: Starts the Minecraft server.
  - `Stop Minecraft Server`: Stops the Minecraft server.
  - `Refresh Server Status`: Fetches and refreshes the Minecraft server info.



## Getting Started

### Prerequisites
Make sure to set the following environment variables:
- `BOT_TOKEN`: Your Discord bot token.
- `MINECRAFT_API_PATH`: The root endpoint of the Minecraft-API project.

You can also use a `.env` file to store these values for local development.

### Running the Project
There are two ways to deploy this project:

1. **Local Development**
   Run the bot locally with Python:
   `python main.py`

2. **Kubernetes Deployment**
Deploy the bot on a Kubernetes cluster using the Helm chart located in the `deploy/` directory.

## Timeline
- Project start: `2024/10/08`
- First working version: `2024/10/09`
- GitLab CI/CD deploy pipeline set up: `2024/10/13`
- Implement persistent views to reduce message re-generation frequency: `2024/10/14`
- GitLab CI/CD build pipeline set up: `2024/10/16`

## Roadmap
- [x] Discord bot implementation
- [x] Server management integration with Minecraft-API
- [x] Kubernetes deployment with Helm chart
- [ ] Add more server control actions
- [ ] Monitoring and logging the server status
- [ ] Manage multiple servers
- [ ] Manage non-minecraft server