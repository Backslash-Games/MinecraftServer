# This example requires the 'message_content' intent.
import sys

import discord
import os

from termcolor import colored as clr

# Set source key
SOURCE_KEY = str(clr("[DISCORD_BOT] ", 'blue'))
# Pull working directory
CWD = os.getcwd()

# Temporary method to pull token from the right folder
def pullToken():
    token_path = os.getcwd() + "/assets/discord_bot/config/token.txt"
    if os.path.exists(token_path):
        log(f"Token path {clr(token_path, 'yellow')} {clr('does', 'green')} exist... Reading information")
        with open(token_path, 'r') as f:
            return f.read()
    log(f"Token path {clr(token_path, 'yellow')} {clr('does not', 'red')} exist... Returning")
    return ""



# ========== Debug ==========
# Definition to print to console
def log(content):
    print(SOURCE_KEY + str(content))



def initializeBot():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        log("Bot is ready")
        return

    @client.event
    async def on_message(message):
        log(f"Bot is has received message {clr(message, 'cyan')}")
        if message.content.startswith('!kill'):
            sys.exit(0)
        return

    token = pullToken()
    client.run(token)
    log("Client has logged out")



# Check for debug arguement
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    initializeBot()