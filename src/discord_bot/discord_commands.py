import os
import sys
import runpy
import discord
from termcolor import colored as clr

# Pull working directory
CWD = os.getcwd()
sys.path.append(CWD + "/src")

import tools.console_formatting as cf
import tools.file_manager as fm
import tools.json_manager as jm

import discord_bot.message_stream as stream

# Setup source
source = cf.Console("DISCORD_COMMANDS", "light_blue")
file_man = fm.FileManager("DISCORD_COMMANDS")
# Setup paths
COMMAND_PATH = CWD + "/assets/discord_bot/commands"
COMMAND_LOG = CWD + "/assets/discord_bot/commands.json"

global commands
commands = {}
check_keys = ['keyword', 'args', 'directory']

# Loads all commands from assets
def loadAllCommands():
    global commands
    # Get all command json files
    json_list = jm.getJsonList(COMMAND_PATH, False)

    source.start_divide("LOADING COMMANDS")
    # Check if commands need to be updated
    if len(json_list) == len(commands):
        source.log(f"No new commands, using list {commands}")
        source.end_divide("USING OLD COMMANDS")
        return

    # Reset command keys
    commands = {}
    # Load each command
    for json in json_list:
        data = jm.getJsonData(COMMAND_PATH + "/" + json, check_keys)
        loadCommand(data)

    # Commands load output
    source.log(f"{len(commands)} commands loaded")
    # source.log(f"Commands: {commands}")

    # Write command information to a json file
    jm.writeJsonData(COMMAND_LOG, jm.toJson(commands))

    source.end_divide("LOADED COMMANDS")
    return
# Load a specific command
def loadCommand(data):
    global commands
    # Write out the json data
    source.log(f"Loading json into commands with data keyword {clr(data['keyword'], 'green')}")
    commands[data['keyword']] = data

# Runs a command
def runCommand(message_data):
    source.start_divide("RUNNING COMMAND")
    keyword = message_data[0]
    # Check if keyword exists
    if not isCommand(keyword):
        source.log(f"No keyword {clr(keyword, 'red')} found")
        return False

    # Check if arguments match
    if not isArgsMatch(message_data[0], len(message_data) - 1):
        source.log(clr("Argument length doesn't match defined", 'red'))
        source.error_divide("ARGUMENT MISMATCH")
        return False

    # Get json file
    source.log(f"Keyword {clr(keyword, 'yellow')} found with associated json file {clr(commands[keyword]['keyword'], 'green')}")

    # Run command
    file_path = CWD + "/" + commands[keyword]['directory']
    if not os.path.exists(file_path):
        source.log(f"Path {file_path} could not be found")
        return False
    # Push through args
    cmd_args = message_data
    cmd_args.pop(0)
    source.log(f"Pushing args {cmd_args}")
    stream.set_args(cmd_args)
    # Run python file
    source.log(f"Running command {clr(keyword, 'green')}")
    runpy.run_path(file_path)

    source.end_divide("COMMAND RUN")
    return True

# Validates command key
def isCommand(key):
    if key in commands:
        source.log(f"Key '{clr(key, 'yellow')}' found")
        return True
    source.log(f"Key '{clr(key, 'yellow')}' does not exist")
    return False

# Checks if the given arguments matches the amount stored in json
def isArgsMatch(keyword, count):
    return str(count) in commands[keyword]['args']

# Process an incoming message
def processMessage(icon, content):
    # Make sure all commands are loaded
    loadAllCommands()

    source.start_divide("PROCESSING MESSAGE")
    # Split up message content
    source.log(f"Processing message with icon {clr(icon, 'green')} and content {clr(content, 'yellow')}")
    content_data = content.split()
    if len(content_data) <= 0:
        source.log(f"Could not process content_data... {content_data}")
        return False
    content_data[0] = content_data[0].replace(icon, "")
    source.log(f"Split and processing message. Using content data... {content_data}")
    source.end_divide("PROCESSED MESSAGE")

    # Run command
    return runCommand(content_data)