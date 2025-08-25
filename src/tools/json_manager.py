import os
import sys
import json
from termcolor import colored as clr

# Pull working directory
CWD = os.getcwd()
sys.path.append(CWD + "/src")

import tools.console_formatting as cf
# Set source
source = cf.Console("JSON_MANAGER", "yellow")

# Gets a list of all jsons in web resources
def getJsonList(path):
    # Holds proper files
    files = []
    for file in os.listdir(path):
        if '.json' in file:
            files.append(file)

    source.log(f"Found json list {clr(files, 'yellow')}")
    return files

# Read information from web-resources json
def getJsonData(file_path, check_keys):
    # Check if the path exists
    if not os.path.exists(file_path):
        return {}

    if not isValidJson(file_path):
        source.log(clr(f"File {file_path} could not be validated... Please check format", 'red', attrs=["reverse", "blink"]))
        return {}

    # Pull information
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Check keys
    check_keys_response = True
    for key in check_keys:
        if not isJsonKey(key, data):
            check_keys_response = False
    if not check_keys_response:
        return {}
    return data

# Gets a json value
def getJsonValue(file_path, key):
    # Check if the path exists
    if not os.path.exists(file_path):
        return ""

    if not isValidJson(file_path):
        source.log(clr(f"File {file_path} could not be validated... Please check format", 'red', attrs=["reverse", "blink"]))
        return ""

    # Pull information
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Check if the key is valid
    if isJsonKey(key, data):
        return data[key]
    return ""

# Writes json data
def writeJsonData(file_path, data):
    # Open file
    with open(file_path, 'w') as f:
        # Write data
        f.write(str(data))
    return

# Writes a single value in json data
def writeJsonValue(file_path, key, value):
    data = getJsonData(file_path, [key])
    data[key] = value
    writeJsonData(file_path, toJson(data))

# Validates json key
def isJsonKey(key, data):
    if key in data:
        source.log(f"Key '{clr(key, 'yellow')}' found [{clr(data[key], 'green')}]")
        return True
    source.log(f"Key '{clr(key, 'yellow')}' does not exist")
    return False

# Checks if a file is a valid json file
def isValidJson(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        source.log(clr(f"Could not validate {file_path} as json... No file found", 'red'))
        return False

    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True
    except ValueError as e:
        source.log(clr(f"Could not validate {file_path} as json...\n{e}", 'red', attrs=["reverse", "blink"]))
    return False

# Validates the json file if it doesnt contain all keys
def validateJsonFile(file_path, check_keys):
    # Pull data from file_path
    data = getJsonData(file_path, check_keys)
    # Check if file needs to be validated
    if data == {}:
        for key in check_keys:
            data[key] = "Information not found, please contact an admin"
        writeJsonData(file_path, toJson(data))

# Turns a dictionary to json
def toJson(dict):
    return json.dumps(dict, indent=4)