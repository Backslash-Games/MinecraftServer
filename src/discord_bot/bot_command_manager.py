import os
import runpy
from termcolor import colored as clr

from src.tools import console_formatting as cf
from src.tools import file_manager as fm
from src.tools import json_manager as jm

from src.discord_bot import message_stream as stream

# Pull working directory
CWD = os.getcwd()

# Setup source
source = cf.Console("DISCORD_COMMANDS", "light_blue")
file_man = fm.FileManager("DISCORD_COMMANDS")
# Setup paths
COMMAND_PATH = CWD + "/assets/discord_bot/commands"
COMMAND_LOG = CWD + "/assets/discord_bot/commands.json"
ADMIN_WHITELIST = CWD + "/assets/discord_bot/config/admin_whitelist.txt"

global commands
commands = {}
check_keys = ['keyword', 'args', 'directory', 'compile', 'require_admin']

# Loads all commands from assets
def loadAllCommands():
    global commands
    # Get all command json files
    json_list = jm.getJsonList(COMMAND_PATH, False, False)

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
    # Check if command should be loaded
    if not data['compile']:
        source.log_error(f"Command '{data['keyword']}' was not loaded, suppressed with compile tag")
        return

    global commands
    # Write out the json data
    source.log(f"Loading json into commands with data keyword {clr(data['keyword'], 'green')}")
    commands[data['keyword']] = data



# Runs a command
def runCommand(message_data, author_data):
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

    # Check if the user can run the command
    if commands[keyword]['require_admin'] and not canUseCommand(author_data):
        stream.send("Invalid permissions, please contact an admin and try again...")
        source.log_error("User has invalid permissions")
        source.error_divide("INVALID PERMISSIONS")
        return False



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
# Validates if a user can run the command
def canUseCommand(author_data):
    # Print out names that we are checking
    source.log(f"Display Name: {author_data.display_name}")
    source.log(f"Global Name: {author_data.global_name}")

    # Check if the user is logged as an admin
    # -> For quick implementation right now, simply check a text file for the users global name
    file_content = file_man.readFile(ADMIN_WHITELIST)
    if author_data.global_name in file_content:
        source.log("User found, running command")
        return True

    # If the user cannot be found then return
    source.log("User not found, stopping command")
    return False


# Checks if the given arguments matches the amount stored in json
def isArgsMatch(keyword, count):
    return str(count) in commands[keyword]['args']



# Process an incoming message
def processMessage(icon, message):
    # Make sure all commands are loaded
    loadAllCommands()

    # Establish content
    content = message.content
    source.start_divide("PROCESSING MESSAGE")
    # Split up message content
    source.log(f"Processing message with icon {clr(icon, 'green')} and content {clr(content, 'yellow')}")
    content_data = split(content)

    if len(content_data) <= 0:
        source.log(f"Could not process content_data... {content_data}")
        return False
    content_data[0] = content_data[0].replace(icon, "")
    source.log(f"Split and processing message. Using content data... {content_data}")
    source.end_divide("PROCESSED MESSAGE")

    # Run command
    return runCommand(content_data, message.author)



# Splits arguments from the sent command
def split(content):
    source.log(f"Splitting Content {content}")
    default_data = content.split()

    content_data = []

    check_token = "||"
    inside_token = False
    temp_value = ""
    # run hi ||tp 0 0 0|| hi
    # Check for pipes
    for value in default_data:
        # If we find the check token in value, and we are outside, move inside the token
        if check_token in value and not inside_token:
            inside_token = True
        # If we find the check token in value, and we are inside, move outside the token
        elif check_token in value and inside_token:
            inside_token = False
            value = temp_value + value
            temp_value = ""

        # Add value to content data
        if not inside_token:
            value = value.replace("||", "")
            content_data.append(value)
        else:
            temp_value += value + " "


    source.log(f"Split content {content_data}")
    return content_data