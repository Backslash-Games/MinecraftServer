# This code will do NOTHING but download the server if it is missing
import subprocess
import os
import sys
import gdown
import shutil

from termcolor import colored as clr
from src.tools import console_formatting as cf
from src.tools import json_manager as jm

# Pull working directory
CWD = os.getcwd()

# Set source
source = cf.Console("WEB_INSTALLER", "cyan")



# Hold a constant for the web resource path
WEB_RESOURCE_DIRECTORY = CWD + "/assets/web-resources"
WEB_RESOURCE_CONFIG = CWD + "/assets/web-resources/config/install_config.json"


# ========== Main Methods ==========
# Downloads all queued resources
def installAllResources():
    # Get a list of all json files
    install_list = jm.getJsonValue(WEB_RESOURCE_CONFIG, "install")
    available_list = jm.getJsonList(WEB_RESOURCE_DIRECTORY, True, False)

    json_list = []
    # Compare install list to json list
    for val in install_list:
        if val in available_list:
            json_list.append(val)

    # Run through the list of json files and check if it needs to be installed
    reinstall_list = jm.getJsonValue(WEB_RESOURCE_CONFIG, "reinstall")
    source.log(reinstall_list)
    for json in json_list:
        # Check reinstall
        check_reinstall = json in reinstall_list
        if check_reinstall:
            source.log(f"{json} found for reinstall")
        # Try to install
        installResource(json, check_reinstall)

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
def installResource(json, reinstall):
    # Notify that the installation process has started
    source.start_divide(f"Started install of {json}")


    # Pull data
    file_path = WEB_RESOURCE_DIRECTORY + "/" + json
    check_keys = ['url', 'type', 'source', 'dir', 'file', 'folder_expected_files']
    data = jm.getJsonData(file_path, check_keys)
    installed = is_installed(data)


    # Hold constant data
    install_url = data['url']
    install_type = data['type']
    install_source = data['source']
    install_directory = CWD + data['dir']
    install_file_path = install_directory + data['file']
    install_file_name = data['file'].replace('/', '')


    # Check if the data is installed or needs a re-installation
    if installed and not reinstall:
        source.end_divide(f"Canceled install of {json}")
        return
    elif installed and reinstall:
        if install_type == "file":
            uninstall(install_file_path)
        elif install_type == "folder":
            remove_directory(install_directory)
        source.log(f"Reinstalling {json}")


    # Run install
    response = installUsingSource(install_url, install_source, install_directory, install_file_path, install_file_name)
    if not response:
        source.error_divide(f"{clr("Failed install", 'red')} of {json}")
        return

    # If we are installing a folder and it is successful... log the expected file value
    if install_type == "folder":
        installed_length = len(os.listdir(install_directory))
        source.log(f"Setting expected files to {installed_length}")
        jm.writeJsonValue(file_path, "folder_expected_files", installed_length)

    # Notify that the installation process has stopped
    source.end_divide(f"Finished install of {json}")
    return



# Runs different install methods based on source
def installUsingSource(url, source, directory, file_path, file_name):
    # Use a tree to check source
    match source:
        case 'minecraft':
            return installWGet(url, directory, file_path)
        case 'drive':
            return installGDown(url, file_path)
        case 'drive_folder':
            return install_gdown_folder(url, directory)

    source.log(f"No statements with {clr(source, 'yellow')} exist")
    return False



# Install using wget
# --> Source == 'minecraft'
def installWGet(url, directory, file_name):
    source.log(f"Using {clr('wget', 'light_blue')} to download... This may take a moment")

    # Install the content
    try:
        # Run the download
        install_response = subprocess.check_output(["wget", "-P", directory, url, "-O", file_name], text=True)
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

# Install using gdown folder
# --> Source == 'drive'
def install_gdown_folder(url, dir):
    # Uninstall previous folder if it exists
    remove_directory(dir)

    # Install
    source.log(f"Using {clr('gdown_folder', 'light_blue')} to download... This may take a moment")
    gdown.download_folder(url, output=dir)
    return True

def uninstall(file_path):
    # Uninstall log
    source.log(f"Uninstalling file at path {clr(file_path, 'yellow')}")

    # Uninstall the file
    try:
        # Run the download
        install_response = subprocess.check_output(["rm", file_path], text=True)
        source.log(install_response)

    # Error if the server cannot be installed due to the sub process
    except subprocess.CalledProcessError as e:
        source.log({clr(f"rm failed with exception {e.returncode}", 'red')})
        return False

    return

def remove_directory(directory):
    # Make sure path exists
    if os.path.exists(directory) and os.path.isdir(directory):
        try:
            shutil.rmtree(directory)
            source.log(f"Removed folder and contents at {directory}")
        except OSError as e:
            source.log(f"Error at {directory} : {e.strerror}")
    return

# ========== Checks ==========
# Checks if the data is already installed
def is_installed(data):
    data_directory = CWD + data['dir']
    data_file_path = data_directory + data['file']
    data_type = data['type']
    source.log(f"Data type is {data_type}")

    # Check directory
    if os.path.isdir(data_directory):
        source.log(f"Directory {clr(data_directory, 'yellow')} {clr('does', 'green')} exist... Checking file {clr(data['file'], 'yellow')}")

        # Check if expected files are correct
        if data_type == "folder":
            source.log("No file check needed, is folder")
            data_expected_files = data['folder_expected_files']

            if data_expected_files == count_contained_files(data_directory):
                source.log(f"Directory {clr(data_directory, 'yellow')} contains the correct number of files {data_expected_files}")
                return True
            else:
                source.log_error(f"Directory {data_directory} does not contain the correct number of files {data_expected_files}")
                return False
    # Otherwise Log
    else:
        source.log(f"Directory {clr(data_directory, 'yellow')} {clr('does not', 'red')} exist... Creating now")
        if not createDirectory(data_directory):
            source.log(f"Directory {clr(data_directory, 'yellow')} could not be created... Returning {clr('false', 'red')}")
            return False


    # Check file path
    if os.path.exists(data_file_path) and data_type == "file":
        source.log(f"File {clr(data_file_path, 'yellow')} {clr('does', 'green')} exist... Returning {clr('true', 'green')}")
        return True
    # Otherwise Log
    else:
        source.log(f"File {data_file_path} {clr('does not', 'red')} exist... Returning {clr('false', 'red')}")


    return False

def count_contained_files(directory):
    # Ensure the given value is a directory
    if not os.path.exists(directory) or not os.path.isdir(directory):
        source.log_error(f"Path {directory} is not a directory")
        return 0

    directory_list = os.listdir(directory)
    file_count = 0

    source.log(f"Counting entries...")
    for val in directory_list:
        # Check if the path is a file
        if os.path.isfile(f"{directory}/{val}"):
            file_count += 1
    source.log(f"Found {file_count} entries in {directory}")

    return file_count



# Check for debug arguement
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    installAllResources()