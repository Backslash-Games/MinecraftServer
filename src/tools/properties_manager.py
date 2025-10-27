import os
from termcolor import colored as clr

# ========== TOOL SETUP ==========
from . import console_formatting as cf

CWD = os.getcwd()
# MAIN GOAL - set up properties into a dictionary that can be quickly accessed
class PropertiesManager:
    @staticmethod
    def parse(contents):
        # Create a new dictionary
        properties = {}
        # Go through each line of the given string
        for line in contents.splitlines():
            # Check for commeted out data
            if line[0] == "#":
                continue
            # Parse into readable data
            value = line.split("=", 1)
            # Make sure the value is the right size
            if len(value) != 2:
                continue
            properties[value[0]] = value[1]
        # Return data
        return properties