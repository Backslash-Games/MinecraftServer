import web_validation.web_installer as installer
import discord_bot.discord_boot as bot
import tools.run_jar as jar
import tools.console_formatting as cf
import multiprocessing

import os

from termcolor import colored as clr

# Define local format
source = cf.Console("MAIN", "green")
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
source.log("Initializing Discord Process")
discord_process = multiprocessing.Process(target=bot.runBot)

# Start up processes
source.log("Starting Server Process")
server_process.start()
discord_process.start()

# Check if processes have finished
server_process.join()
discord_process.join()


# Debug output
i = 50
while i > 0:
    source.log(clr("  !!!!!!    All processes have stopped    !!!!!!  ", 'red', attrs=["reverse", "blink"]))
    i = i - 1