# This code will do NOTHING but download the server if it is missing
import subprocess
import os
import sys
import json
import gdown
from termcolor import colored as clr

# Set source key
SOURCE_KEY = str(clr("[WEB_INSTALLER] ", 'cyan'))
# Pull working directory
CWD = os.getcwd()
# Hold a constant for the web resource path
WEB_RESOURCE_DIRECTORY = CWD + "/assets/web-resources"
# Hold formatting constants
LOG_DIVIDER_START = clr("====================", 'green')
LOG_DIVIDER_END = clr("====================", 'red')
LOG_DIVIDER_CANCELED = clr("====================", 'yellow')


# ========== Main Methods ==========
# Downloads all queued resources
def installAllResources():
    # Get a list of all json files
    json_list = getJsonList()

    # Run through the list of json files and check if it needs to be installed
    for json in json_list:
        # Try to install
        installResource(json)

    return



# Create directory
def createDirectory(path):
    # Create the directory
    os.mkdir(path)

    # Double check that the directory exists
    if not os.path.exists(path):
        return False

    return True



# ========== Install Methods ==========
# Downloads one resource
def installResource(json):
    # Notify that the installation process has started
    log('')
    log(f"{LOG_DIVIDER_START} Started install of {clr(json, 'yellow')} {LOG_DIVIDER_START}")


    # Pull data
    data = getJsonData(json)
    # Check if the data is installed
    if isInstalled(data):
        log(f"{LOG_DIVIDER_CANCELED} Canceled install of {clr(json, 'yellow')} {LOG_DIVIDER_CANCELED}")
        log('')
        return


    # Install data
    install_url = data['url']
    install_source = data['source']
    install_directory = CWD + data['dir']
    install_file_path = install_directory + data['file']


    # Run install
    response = installUsingSource(install_url, install_source, install_directory, install_file_path)
    if not response:
        log(f"{LOG_DIVIDER_CANCELED} {clr("Failed install", 'red')} of {clr(json, 'yellow')} {LOG_DIVIDER_CANCELED}")
        log('')
        return


    # Notify that the installation process has stopped
    log(f"{LOG_DIVIDER_END} Finished install of {clr(json, 'yellow')} {LOG_DIVIDER_END}")
    log('')
    return



# Runs different install methods based on source
def installUsingSource(url, source, dir, file_path):
    # Use a tree to check source
    match source:
        case 'minecraft':
            return installWGet(url, dir)
        case 'drive':
            return installGDown(url, file_path)

    log(f"No statements with {clr(source, 'yellow')} exist")
    return False



# Install using wget
# --> Source == 'minecraft'
def installWGet(url, dir):
    log(f"Using {clr('wget', 'light_blue')} to download... This may take a moment")

    # Install the content
    try:
        # Run the download
        install_response = subprocess.check_output(["wget", "-P", dir, url], text=True)
        log(install_response)

    # Error if the server cannot be installed due to the sub process
    except subprocess.CalledProcessError as e:
        log({clr(f"wget failed with exception {e.returncode}", 'red')})
        return False

    return True

# Install using gdown
# --> Source == 'drive'
def installGDown(url, file_path):
    log(f"Using {clr('gdown', 'light_blue')} to download... This may take a moment")
    gdown.download(url, file_path, fuzzy=True)
    return True


# ========== Get Methods ==========
# Gets a list of all jsons in web resources
def getJsonList():
    # Holds proper files
    files = []
    for file in os.listdir(WEB_RESOURCE_DIRECTORY):
        if '.json' in file:
            files.append(file)

    log(f"Found json list {clr(files, 'yellow')}")
    return files

# Read information from web-resources json
def getJsonData(file):
    # Get reference to the current file path
    path = WEB_RESOURCE_DIRECTORY + "/" + file

    # Check if the path exists
    if not os.path.exists(path):
        return {}

    # Pull information
    with open(path, 'r') as f:
        data = json.load(f)

    # Check keys
    check_keys = ['url', 'source', 'dir', 'file']
    check_keys_response = True
    for key in check_keys:
        if not isJsonKey(key, data):
            check_keys_response = False
    if not check_keys_response:
        return {}
    return data


# ========== Checks ==========
# Validates json key
def isJsonKey(key, data):
    if key in data:
        log(f"- Key '{clr(key, 'yellow')}' found [{clr(data[key], 'green')}]")
        return True
    log(f"Key '{clr(key, 'yellow')}' does not exist")
    return False




# Checks if the data is already installed
def isInstalled(data):
    data_directory = CWD + data['dir']
    data_file_path = data_directory + data['file']


    # Check directory
    if os.path.isdir(data_directory):
        log(f"Directory {clr(data_directory, 'yellow')} {clr('does', 'green')} exist... Checking file {clr(data['file'], 'yellow')}")
    # Otherwise Log
    else:
        log(f"Directory {clr(data_directory, 'yellow')} {clr('does not', 'red')} exist... Creating now")
        if not createDirectory(data_directory):
            log(f"Directory {clr(data_directory, 'yellow')} could not be created... Returning {clr('false', 'red')}")
            return


    # Check file path
    if os.path.exists(data_file_path):
        log(f"File {clr(data_file_path, 'yellow')} {clr('does', 'green')} exist... Returning {clr('true', 'green')}")
        return True
    # Otherwise Log
    else:
        log(f"File {clr(data_file_path, 'yellow')} {clr('does not', 'red')} exist... Returning {clr('false', 'red')}")


    return False


# ========== Debug ==========
# Definition to print to console
def log(content):
    print(SOURCE_KEY + str(content))




# Check for debug arguement
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    installAllResources()