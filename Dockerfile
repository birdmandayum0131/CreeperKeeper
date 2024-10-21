FROM python:3.11.10-alpine
LABEL author="Bird"
# Create a non-root user and set the home directory
RUN addgroup -S Servers && adduser -S discordbot -G Servers
# Switch to the non-root user
USER discordbot
# Create the server directory
RUN mkdir /home/discordbot/CreeperKeeper
COPY ./ /home/discordbot/CreeperKeeper
RUN pip install -r /home/discordbot/CreeperKeeper/requirements.txt
# Copy server file and eula to the image for building
WORKDIR /home/discordbot/CreeperKeeper
CMD ["python", "./src/main.py"]