import web_validation.web_installer as installer
import java_management.run_jar as jar
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
log(clr("DISCORD NOT YET IMPLEMENTED", 'red'))

# Start up processes
log("Starting Server Process")
server_process.start()

# Check if processes have finished
server_process.join()



# Debug output
i = 30
while i > 0:
    log(clr("  !!!!!!    All processes have stopped    !!!!!!  ", 'red', attrs=["reverse", "blink"]))
    i = i - 1