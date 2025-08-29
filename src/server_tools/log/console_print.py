import os
import sys

CWD = os.getcwd()
sys.path.append(CWD + "/src")

import tools.console_formatting as cf
source = cf.Console("SERVER", 'blue')

SERVER_LOGS_PATH = CWD + "/server/logs"
SERVER_LOGS_FILEPATH = SERVER_LOGS_PATH + "/latest.log"

READ_INDEX = 0

STOP_STRING = "[Server thread/INFO]: Stopping server"
STOP_INDEX = False

# Updates the console with the server logs
def printServerLogs():
    # Check if the server exists at this point
    if not os.path.exists(SERVER_LOGS_PATH):
        source.log(f"Could not find directory {SERVER_LOGS_PATH}")
        return

    # Check if the file exists
    if not os.path.exists(SERVER_LOGS_FILEPATH):
        source.log(f"Could not find file {SERVER_LOGS_FILEPATH}")
        return

    global READ_INDEX
    global STOP_STRING
    global STOP_INDEX

    # Pull unseen lines and print
    with open(SERVER_LOGS_FILEPATH, 'r') as file:
        # Get all lines
        lines = file.readlines()

        # Shear out read lines
        split_lines = lines[READ_INDEX:]
        READ_INDEX = len(lines)

        # Print out lines
        for line in split_lines:
            source.log(line.replace("\n", ""))

            # Check if the server is stopping
            if STOP_STRING in line:
                STOP_INDEX = True


def clear_log():
    # Check if the server exists at this point
    if not os.path.exists(SERVER_LOGS_PATH):
        source.log_error(f"Could not find directory {SERVER_LOGS_PATH}")
        return

    # Check if the file exists
    if not os.path.exists(SERVER_LOGS_FILEPATH):
        source.log_error(f"Could not find file {SERVER_LOGS_FILEPATH}")
        return

    # Open file and clear
    with open(SERVER_LOGS_FILEPATH, 'w') as file:
        file.write("")

    source.log("Cleared Logs")

# Run start method
def on_start():
    clear_log()

# Run server logs on a loop
def on_update():
    global READ_INDEX
    global STOP_STRING
    global STOP_INDEX

    printServerLogs()