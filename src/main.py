import web_validation.web_installer as installer
import java_management.run_jar as jar
import discord_bot.bot_initialization as bot
import multiprocessing

import os

from termcolor import colored as clr

# Set source key
SOURCE_KEY = str(clr("[MAIN] ", 'green'))
# Pull working directory
CWD = os.getcwd()


# ========== Debug ==========
# Definition to print to console
def log(content):
    print(SOURCE_KEY + str(content))



# When started, install all content using the web-installer
log("Installing all resources")
installer.installAllResources()



# Initialize Processes
# -> Server process
log("Initializing Server Process")
server_process = multiprocessing.Process(target=jar.runJar, args=("/server", "/server.jar"))
log("Initializing Discord Process")
discord_process = multiprocessing.Process(target=bot.initializeBot)

# Start up processes
log("Starting Server Process")
server_process.start()
discord_process.start()

# Check if processes have finished
server_process.join()
discord_process.join()


# Debug output
i = 50
while i > 0:
    log(clr("  !!!!!!    All processes have stopped    !!!!!!  ", 'red', attrs=["reverse", "blink"]))
    i = i - 1