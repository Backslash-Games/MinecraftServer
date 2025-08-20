# This code will do NOTHING but download the server if it is missing
import subprocess
import os
import sys
import json
from termcolor import colored as clr

# Set source key
SOURCE_KEY = str(clr("[WEB-INSTALLER] ", 'cyan'))
# Pull working directory
CWD = os.getcwd()
# Hold a constant for the web resource path
WEB_RESOURCE_DIRECTORY = CWD + "/assets/web-resources"

# Gets a list of all jsons in web resources
def getJsonList():
    # Holds proper files
    files = []
    for file in os.listdir(WEB_RESOURCE_DIRECTORY):
        if '.json' in file:
            files.append(file)
    return files

# Read information from web-resources json
def getJsonData(file):
    # Get reference to the current file path
    path = WEB_RESOURCE_DIRECTORY + "/" + file

    # Check if the path exists
    if not os.path.exists(path):
        return ['', '', '']

    # Pull information
    with open(path, 'r') as f:
        data = json.load(f)

    # Check keys
    if isJsonKey('url', data) and  isJsonKey('dir', data) and isJsonKey('file', data):
        return [data['url'], data['dir'], data['file']]
    return ['', '', '']

# Validates json key
def isJsonKey(key, data):
    if key in data:
        log(f"- Key '{key}' found [{data[key]}]")
        return True
    log(f"Key '{key}' does not exist")
    return False

# Definition to print to console
def log(content):
    print(SOURCE_KEY + str(content))

log("JSON LIST")
log(getJsonList())
print()
log("JSON DATA")
log(getJsonData("server.json"))
sys.exit(0)

# Set constants
SERVER_INSTALL_CONFIG_PATH = CWD + "/config/server-install-url.txt"
SERVER_DIRECTORY = CWD + "/server"
SERVER_PATH = SERVER_DIRECTORY + "/server.jar"
EULA_PATH = SERVER_DIRECTORY + "/eula.txt"

REINSTALL_COMMAND = "--force-reinstall"


# Check if the server already exists
argument_count = len(sys.argv)
if os.path.isdir(SERVER_DIRECTORY) and ((argument_count > 1 and sys.argv[1] != REINSTALL_COMMAND) or argument_count == 1):
    print("server-setup.py --> Server already exists, skipping install... to force reinstall use " + str(REINSTALL_COMMAND))
    sys.exit(0)
elif os.path.isdir(SERVER_DIRECTORY) and argument_count > 1 and sys.argv[1] == REINSTALL_COMMAND:
    # Destroy the server
    response = subprocess.check_output(["rm", "-r", SERVER_DIRECTORY], text=True)
    print(response)



# Pull the URL
url_file = open(SERVER_INSTALL_CONFIG_PATH, 'r')
url = url_file.read()
url_file.close()



# Install the server
try:
    # Run the download
    response = subprocess.check_output(["wget", "-P", SERVER_DIRECTORY, url], text=True)
    print(response)

# Error if the server cannot be installed due to the sub process
except subprocess.CalledProcessError as e:
    print(f"server-setup.py --> Failed with return {e.returncode}")