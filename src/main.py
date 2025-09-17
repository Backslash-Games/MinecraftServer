import os
import time
import multiprocessing
import subprocess

from termcolor import colored as clr

from src import RESTART_ON_CLOSE
from src.discord_bot import bot_start as bot
from src.server_tools import server_manager as server_man

from src.tools import console_formatting as cf
from src.tools import jar_manager as jar

from src.web_validation import installer

# Define local format
source = cf.Console("MAIN", "light_magenta")
# Reset runtime logs
source.resetRuntimeLogs()
# Pull working directory
CWD = os.getcwd()


# When started, install all content using the web-installer
source.log("Installing all resources")
installer.install_all()



# Initialize Processes
# -> Server process
source.log("Initializing Server Process")
server_process = multiprocessing.Process(target=jar.runJar, args=("/server", "/server.jar"))

source.log("Initializing Server Print Process")
server_log_process = multiprocessing.Process(target=server_man.run_manager_loop)

source.log("Initializing Discord Process")
discord_process = multiprocessing.Process(target=bot.runBot)



# Start up processes
source.log("Starting Server Process")
server_process.start()

source.log("Starting Server Print Process")
server_log_process.start()

source.log("Starting Discord Bot Process")
discord_process.start()



# Check if processes have finished
source.log("Joining Server Process")
server_process.join()

source.log_error("KILLING ALL PROCESSES")

source.log("Joining Server Print Process")
server_log_process.terminate()
server_log_process.join()

source.log("Joining Discord Bot Process")
discord_process.terminate()
discord_process.join()


# Debug output
i = 20
while i > 0:
    source.log(clr(f"  !!!!!!    All processes have stopped... Restarting in {round(i / 4)}    !!!!!!  ", 'red', attrs=["reverse", "blink"]))
    i = i - 1
    time.sleep(0.25)

# Restart the server
if RESTART_ON_CLOSE:
    subprocess.check_output(["reboot"])