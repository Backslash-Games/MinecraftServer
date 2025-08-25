# This code will do NOTHING but download the server if it is missing
import subprocess
import os
import sys
import json
import gdown
from termcolor import colored as clr

# Pull working directory
CWD = os.getcwd()
sys.path.append(CWD + "/src")

import tools.console_formatting as cf
import tools.json_manager as jm

# Set source
source = cf.Console("WEB_INSTALLER", "cyan")




# Hold a constant for the web resource path
WEB_RESOURCE_DIRECTORY = CWD + "/assets/web-resources"


# ========== Main Methods ==========
# Downloads all queued resources
def installAllResources():
    # Get a list of all json files
    json_list = jm.getJsonList(WEB_RESOURCE_DIRECTORY)

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
    source.start_divide(f"Started install of {json}")


    # Pull data
    file_path = WEB_RESOURCE_DIRECTORY + "/" + json
    check_keys = ['url', 'source', 'dir', 'file']
    data = jm.getJsonData(file_path, check_keys)
    # Check if the data is installed
    if isInstalled(data):
        source.end_divide(f"Canceled install of {json}")
        return


    # Install data
    install_url = data['url']
    install_source = data['source']
    install_directory = CWD + data['dir']
    install_file_path = install_directory + data['file']


    # Run install
    response = installUsingSource(install_url, install_source, install_directory, install_file_path)
    if not response:
        source.error_divide(f"{clr("Failed install", 'red')} of {json}")
        return


    # Notify that the installation process has stopped
    source.end_divide(f"Finished install of {json}")
    return



# Runs different install methods based on source
def installUsingSource(url, source, dir, file_path):
    # Use a tree to check source
    match source:
        case 'minecraft':
            return installWGet(url, dir)
        case 'drive':
            return installGDown(url, file_path)

    source.log(f"No statements with {clr(source, 'yellow')} exist")
    return False



# Install using wget
# --> Source == 'minecraft'
def installWGet(url, dir):
    source.log(f"Using {clr('wget', 'light_blue')} to download... This may take a moment")

    # Install the content
    try:
        # Run the download
        install_response = subprocess.check_output(["wget", "-P", dir, url], text=True)
        source.log(install_response)

    # Error if the server cannot be installed due to the sub process
    except subprocess.CalledProcessError as e:
        source.log({clr(f"wget failed with exception {e.returncode}", 'red')})
        return False

    return True

# Install using gdown
# --> Source == 'drive'
def installGDown(url, file_path):
    source.log(f"Using {clr('gdown', 'light_blue')} to download... This may take a moment")
    gdown.download(url, file_path, fuzzy=True)
    return True

# ========== Checks ==========
# Checks if the data is already installed
def isInstalled(data):
    data_directory = CWD + data['dir']
    data_file_path = data_directory + data['file']


    # Check directory
    if os.path.isdir(data_directory):
        source.log(f"Directory {clr(data_directory, 'yellow')} {clr('does', 'green')} exist... Checking file {clr(data['file'], 'yellow')}")
    # Otherwise Log
    else:
        source.log(f"Directory {clr(data_directory, 'yellow')} {clr('does not', 'red')} exist... Creating now")
        if not createDirectory(data_directory):
            source.log(f"Directory {clr(data_directory, 'yellow')} could not be created... Returning {clr('false', 'red')}")
            return


    # Check file path
    if os.path.exists(data_file_path):
        source.log(f"File {clr(data_file_path, 'yellow')} {clr('does', 'green')} exist... Returning {clr('true', 'green')}")
        return True
    # Otherwise Log
    else:
        source.log(f"File {clr(data_file_path, 'yellow')} {clr('does not', 'red')} exist... Returning {clr('false', 'red')}")


    return False





# Check for debug arguement
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    installAllResources()