import os

from src.tools import console_formatting as cf
from src.tools import json_manager as jm
from src.discord_bot import message_stream as stream

# Define final variables
CWD = os.getcwd()
KEY = "ADMIN"
ADMIN_WHITELIST = CWD + "/assets/discord_bot/config/admin_whitelist.json"
# Define Logger
source = cf.Console(KEY, "magenta")

# Pull all arguments
cmd_args = stream.get_args()



# Adds an admin
def add_admin(name):
    # Pull admin list
    admin_list = jm.getJsonValue(ADMIN_WHITELIST, "white_list")

    # Check if the process goes through
    if name in admin_list:
        return_string = f":warning: {name} is in admin list, returning early"
        source.log_warning(return_string)
        stream.send(return_string)
        return

    # Add
    admin_list.append(name)
    # Rewrite
    jm.writeJsonValue(ADMIN_WHITELIST, "white_list", admin_list)

    # Ping user
    return_string = f":white_check_mark: Successfully added {name} to admin whitelist."
    source.log_error(return_string)
    stream.send(return_string)

# Removes an admin
def remove_admin(name):
    # Pull admin list
    admin_list = jm.getJsonValue(ADMIN_WHITELIST, "white_list")

    # Check if the process goes through
    if not(name in admin_list):
        return_string = f":x: {name} is not in admin list, returning early"
        source.log_error(return_string)
        stream.send(return_string)
        return
    # Check if there is only one admin, if so then dont allow removal
    if len(admin_list) == 1:
        return_string = f":x: Only 1 admin remains, cannot remove... Please contact {admin_list[0]} for help..."
        source.log_error(return_string)
        stream.send(return_string)
        return

    # Remove
    admin_list.remove(name)
    # Rewrite
    jm.writeJsonValue(ADMIN_WHITELIST, "white_list", admin_list)

    # Ping user
    return_string = f":white_check_mark: Successfully removed {name} to admin whitelist."
    source.log_error(return_string)
    stream.send(return_string)




# Check which path we are taking
if cmd_args[0] == "add" and len(cmd_args) == 2:
    source.log("Adding admin")
    add_admin(cmd_args[1])
elif cmd_args[0] == "remove" and len(cmd_args) == 2:
    source.log("Removing admin")
    remove_admin(cmd_args[1])
elif cmd_args[0] == "list" and len(cmd_args) == 1:
    return_string = jm.getJsonValue(ADMIN_WHITELIST, "white_list")
    source.log_error(return_string)
    stream.send(return_string)
else:
    return_string = f":x: Command {cmd_args[1]} is not a valid command."
    source.log_error(return_string)
    stream.send(return_string)