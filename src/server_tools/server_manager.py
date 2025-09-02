# Handles management for processes tied to the server
# -> Running Minecraft Commands
# -> Console Printing
import os
import time

import src.tools.console_formatting as cf

# Import files to manage
import src.server_tools.log.console_print as console_print
import src.server_tools.bridge.bridge_communication_manager as mc_command

CWD = os.getcwd()
source = cf.Console("SERVER_MANAGER", 'red')

# Run start methods
def run_start():
    console_print.clear_log()

# Run update methods
def run_update():
    # mc_command.on_update()
    console_print.on_update()

SLEEP_TIME = 1
RUNNING = True
# Run the manager loop
def run_manager_loop():
    # Start
    run_start()
    # Update Loop
    global SLEEP_TIME
    global RUNNING
    while RUNNING:
        run_update()
        # Check for a stop
        RUNNING = not console_print.STOP_INDEX
        time.sleep(SLEEP_TIME)
    source.log_error("!!!!! MANAGER THREAD STOPPED !!!!!")