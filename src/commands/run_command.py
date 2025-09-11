import os
import sys
import time

CWD = os.getcwd()
sys.path.append(CWD + "/src")

import tools.console_formatting as cf
source = cf.Console("RUN_COMMAND", 'cyan')

import discord_bot.message_stream as stream
import server.bridge.minecraft_command

cmd_args = stream.get_args()
source.log(f"Found arguments {cmd_args}")
# Check if args should be set to default
if len(cmd_args) <= 0:
    source.log_error("Not enough arguments")
    sys.exit(0)

# Send message
server.bridge.minecraft_command.add_command(cmd_args[0])