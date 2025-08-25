import os
import sys
from termcolor import colored as clr


# ========== TOOL SETUP ==========
CWD = os.getcwd()
sys.path.append(CWD + "/src/tools")
import console_formatting as cf

# MAIN GOAL - Quickly pull and push information to files stored in /assets
class FileManager:
    # define root source
    KEY = "FILE_MANAGEMENT"
    COLOR = "light_grey"

    route = "UNKNOWN"
    source = cf.Console(KEY, COLOR)
    CWD = os.getcwd()

    def __init__(self, route):
        self.setRoute(route)
        return

    # Updates the source key
    def updateSourceKey(self):
        self.source.setSourceKeyRoute(self.KEY, self.route, self.COLOR)

    # Sets the route
    def setRoute(self, route):
        self.route = route
        self.updateSourceKey()

    # If file exists return all information contained
    def readFile(self, path):
        if not self.exists(path):
            self.source.log(clr(f"Could not complete readFile({path})", 'red'))
            return ''
        with open(path, 'r') as file:
            return file.read()

    def writeFile(self, path, content):
        return

    # Check if file at path exists
    def exists(self, path):
        # Check if the file exists
        if os.path.exists(path):
            self.source.log(f"File at path '{clr(path, 'yellow')}' {clr("exists", 'green')}")
            return True
        self.source.log(f"File at path '{clr(path, 'yellow')}' {clr("does not exist", 'red')}")
        return False