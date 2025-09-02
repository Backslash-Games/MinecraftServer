import os

from src.tools import console_formatting as cf
from src.tools import json_manager as jm

CWD = os.getcwd()

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