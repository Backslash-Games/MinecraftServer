import os
import sys

CWD = os.getcwd()
sys.path.append(CWD + "/src")

from termcolor import colored as clr

import tools.json_manager as jm
import tools.console_formatting as cf

source = cf.Console("MESSAGE_STREAM", "green")

MESSAGE_STREAM_PATH = CWD + "/assets/discord_bot/message_stream.json"

CHECK_KEYS = ['queued', 'message', 'args']

# Queue message to send
def send(message):
    jm.validateJsonFile(MESSAGE_STREAM_PATH, CHECK_KEYS)
    jm.writeJsonValue(MESSAGE_STREAM_PATH, "queued", True)
    jm.writeJsonValue(MESSAGE_STREAM_PATH, "message", message)

# Define arguments
def set_args(cmd_args):
    jm.validateJsonFile(MESSAGE_STREAM_PATH, CHECK_KEYS)
    jm.writeJsonValue(MESSAGE_STREAM_PATH, "args", cmd_args)
# Get arguments
def get_args():
    return jm.getJsonValue(MESSAGE_STREAM_PATH, CHECK_KEYS[2])

# Checks if the stream is queued
def isQueued():
    return jm.getJsonValue(MESSAGE_STREAM_PATH, CHECK_KEYS[0])

# Get queued data
def getStoredData():
    jm.validateJsonFile(MESSAGE_STREAM_PATH, CHECK_KEYS)
    response = jm.getJsonData(MESSAGE_STREAM_PATH, CHECK_KEYS)
    jm.writeJsonValue(MESSAGE_STREAM_PATH, "queued", False)
    return response

# Validates data file
# -> Will always return true. Fixes problems if any are found
def validataDataFile(path):
    if not jm.isValidJson(path):
        resetMessageStream()
    return True

# Resets json data in message stream
def resetMessageStream():
    default_stream = {}
    for value in CHECK_KEYS:
        default_stream[value] = "Information not found, please contact an admin."
    # Push to file
    jm.writeJsonData(MESSAGE_STREAM_PATH, jm.toJson(default_stream))
    return