import os
import sys
import json

CWD = os.getcwd()
sys.path.append(CWD + "/src")

import discord_bot.message_stream as stream

COMMAND_LOG_FILE = CWD + "/assets/discord_bot/commands.json"

if os.path.exists(COMMAND_LOG_FILE):
    # Pull data from commands.json
    with open(COMMAND_LOG_FILE, 'r') as f:
        data = json.load(f)
    keys = list(data.keys())
    print(keys)

    # Organize information
    message = ""
    for key in keys:
        message = f"{message}\n- {key}"
    # Write message
    stream.send(message)