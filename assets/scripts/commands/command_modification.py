import os
import sys

CWD = os.getcwd()
sys.path.append(CWD + "/src")

import discord_bot.discord_commands as commands
import discord_bot.message_stream as stream

import tools.console_formatting as cf
import tools.json_manager as jm
source = cf.Console("COMMAND COMMAND", 'red')


# Update the discord commands
def update_commands():
    commands.commands = {}
    commands.loadAllCommands()



def validate_args(check_index, valid_args, default_index):
    source.log(cmd_args)
    source.log(check_index)
    source.log(valid_args)
    source.log(valid_args[default_index])
    if len(cmd_args) > check_index:
        # Make sure cmd arg is valid
        if cmd_args[check_index] in valid_args:
            return cmd_args[check_index]
    return valid_args[default_index]



TARGET_ARGS = ["-d", "-f"]
def get_target():
    return validate_args(2, TARGET_ARGS, 1)

SOURCE_ARGS = ["-j", "-m", "-s"]
def get_source():
    return validate_args(3, SOURCE_ARGS, 0)

MODIFY_MODE_ARGS = ["-c", "-v", "-e", "-r", "-d"]
def get_modify_mode():
    return validate_args(4, MODIFY_MODE_ARGS, 1)

def get_file_contents(path):
    if not os.path.exists(path):
        return "file not found"
    with open(path, 'r') as f:
        response = f.read()
    return response

JSON_PATH = CWD + "/assets/discord_bot/commands"
COMMAND_LOG_FILE = CWD + "/assets/discord_bot/commands.json"
def view_file(cmd_name, cmd_source):
    # Check if the source is json
    if cmd_source == "-j":
        check_path = JSON_PATH + "/" + cmd_name + ".json"
        return get_file_contents(check_path)
    # Check if the source is json
    if cmd_source == "-m" or cmd_source == "-s":
        cmd_data = jm.getJsonValue(COMMAND_LOG_FILE, cmd_name)
        if cmd_source == "-m":
            check_path = CWD + cmd_data['manual_directory']
            return get_file_contents(check_path)
        if cmd_source == "-s":
            check_path = CWD + cmd_data['directory']
            return get_file_contents(check_path)
    return f"Could not view file with name {cmd_name} and source {cmd_source}"

def view_dir(cmd_name, cmd_source):
    # Check if the source is json
    if cmd_source == "-j":
        check_path = JSON_PATH + "/" + cmd_name + ".json"
        return check_path
    # Check if the source is json
    if cmd_source == "-m" or cmd_source == "-s":
        cmd_data = jm.getJsonValue(COMMAND_LOG_FILE, cmd_name)
        if cmd_source == "-m":
            check_path = CWD + cmd_data['manual_directory']
            return check_path
        if cmd_source == "-s":
            check_path = CWD + cmd_data['directory']
            return check_path
    return f"Could not view file with name {cmd_name} and source {cmd_source}"

# Modify commands
def modify_command(cmd_args):
    if len(cmd_args) <= 1:
        return "Could not find modified name"

    # Set up modify information
    mod_info = []
    # -> Name [NO DEFAULT]
    if len(cmd_args) > 1:
        mod_info.append(cmd_args[1])
    # -> Target
    mod_info.append(get_target())
    # -> Source
    mod_info.append(get_source())
    # -> Modify Mode
    mod_info.append(get_modify_mode())

    if mod_info[1] == "-f":
        response = view_file(mod_info[0], mod_info[2])

    if mod_info[1] == "-d":
        response = view_dir(mod_info[0], mod_info[2])

    else:
        response = "Unknown Split"

    return response



def process_command(cmd_args):
    # Check for the update command
    if cmd_args[0] == "update":
        update_commands()
        return "Updating commands"

    # Check for modify command
    if cmd_args[0] == "-m":
        return modify_command(cmd_args)

    return "Invalid operation"

source.start_divide("COMMAND COMMAND")

# Get Arguments
cmd_args = stream.get_args()
source.log(f"Found arguments {cmd_args}")

# Send message
response = process_command(cmd_args)
if len(response) > 2000:
    response = response[0:1991]
    response = response + "..."
stream.send(f"```{response}```")

source.end_divide("COMMAND COMMAND")