import web_validation.web_installer as installer
import discord_bot.discord_boot as bot
import tools.run_jar as jar
import tools.console_formatting as cf
import server.log.console_print as server_print
import multiprocessing

import os

from termcolor import colored as clr

# Define local format
source = cf.Console("MAIN", "light_magenta")
# Reset runtime logs
source.resetRuntimeLogs()
# Pull working directory
CWD = os.getcwd()


# When started, install all content using the web-installer
source.log("Installing all resources")
installer.installAllResources()



# Initialize Processes
# -> Server process
source.log("Initializing Server Process")
server_process = multiprocessing.Process(target=jar.runJar, args=("/server", "/server.jar"))

source.log("Initializing Server Print Process")
server_log_process = multiprocessing.Process(target=server_print.logUpdate)

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

source.log("Joining Server Print Process")
server_log_process.join()

source.log("Joining Discord Bot Process")
discord_process.join()


# Debug output
i = 50
while i > 0:
    source.log(clr("  !!!!!!    All processes have stopped    !!!!!!  ", 'red', attrs=["reverse", "blink"]))
    i = i - 1