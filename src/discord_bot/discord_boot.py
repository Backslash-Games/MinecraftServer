import os
import sys
import discord
from termcolor import colored as clr

# Pull working directory
CWD = os.getcwd()
sys.path.append(CWD + "/src")

import tools.console_formatting as cf
import tools.file_manager as fm
import tools.json_manager as jm

import discord_bot.discord_commands as commands
import discord_bot.message_stream as stream

# Set source.source.log
source = cf.Console("DISCORD_BOT", "green")
# File management
file_man = fm.FileManager("DISCORD_BOOT")

TOKEN_PATH = CWD + "/assets/discord_bot/config/token.txt"

COMMAND_ICON_PATH = CWD + "/assets/discord_bot/config/command_icon.txt"
COMMAND_ICON = ''

# Method to pull token from the right folder
def getToken():
    return file_man.readFile(TOKEN_PATH)

# Method to pull command icon
def getCommandIcon():
    return file_man.readFile(COMMAND_ICON_PATH)
# Method to change command icon
def updateCommandIcon():
    char = getCommandIcon()
    source.log(f"Setting command icon to {char}")
    global COMMAND_ICON
    COMMAND_ICON = char


# Display message
def displayMessage(message):
    source.log(f"Bot is has received message {clr(message, 'cyan')}")

def runBot():
    # Set up the bot
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Set the command icon
        updateCommandIcon()
        source.log("Bot is ready")
        return

    @client.event
    async def on_message(message):
        # Return early if it's the bots own message
        if message.author == client.user:
            if message.content.startswith(clr("kill process", 'red')):
                await message.delete()
                sys.exit(0)
            return

        # Display message
        displayMessage(message)

        # Ensure the message starts with the command icon
        if message.content.startswith(COMMAND_ICON):
            source.start_divide(message.content)

            source.log(f"Found message with icon, {COMMAND_ICON}")
            source.log(f"Message sent with content: {message.content}")
            commands.processMessage(COMMAND_ICON, message)

            # Delete the command message
            # await message.delete()

            # Try to send out a message
            source.log("Checking if the message is queued")
            if stream.isQueued():
                # Reply to the message
                source.log("Getting stored data")
                data = stream.getStoredData()
                source.log(f"Checking if {clr("message", 'yellow')} is a valid json key")
                if jm.isJsonKey("message", data):
                    source.log("Sending message to channel")
                    await message.channel.send(data["message"])
                else:
                    source.log(clr(f"CHECK TO MAKE SURE MESSAGE_STREAM.JSON IS SET PROPERLY", 'red'))

            source.end_divide(message.content)
        return

    token = getToken()
    client.run(token)
    source.log("Client has logged out")
    source.log_error("!!!!! BOT STOPPED !!!!!")



# Check for debug arguement
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    runBot()