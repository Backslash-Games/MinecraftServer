import os
import sys

import src.discord_bot.message_stream as stream

import src.tools.json_manager as jm
import src.tools.console_formatting as cf

source = cf.Console("HELP COMMAND", 'magenta')

CWD = os.getcwd()
COMMAND_LOGS = CWD + "/assets/discord_bot/commands.json"

# Gets the manual for a command
def getManual(keyword):
    # Load commands.json
    data = jm.getJsonData(COMMAND_LOGS, [])
    # Check if keyword exists
    if not jm.isJsonKey(keyword, data):
        source.log("No command found")
        return f"```{keyword} does not exist```"
    if not jm.isJsonKey("manual_directory", data[keyword]):
        source.log("No manual directory defined")
        return f"```{keyword} does not have a manual```"
    # Return manual data
    file_path = CWD + data[keyword]["manual_directory"]
    # Check if file path exists
    if not os.path.exists(file_path):
        source.log("Path does not exist")
        return f"```{keyword} does not have a manual```"

    with open(file_path, 'r') as f:
        manual_data = f.read()
    return manual_data



source.start_divide("HELP COMMAND")

# Get Arguments
cmd_args = stream.get_args()
source.log(f"Found arguments {cmd_args}")
# Check if args should be set to default
if len(cmd_args) <= 0:
    cmd_args = ['help']

# Send message
stream.send(getManual(cmd_args[0]))

source.end_divide("HELP COMMAND")