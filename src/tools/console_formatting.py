import os

from termcolor import colored as clr
from datetime import datetime

# Define a console format object
class Console:
    # Define the source key as a variable that can be accessed globally
    SOURCE_KEY = clr("[NO SOURCE]", "red")
    ASSET_PATH = os.getcwd() + "/assets"
    RUNTIME_LOG_FILEPATH = ASSET_PATH + "/runtime.log"

    def __init__(self, key, color):
        self.setSourceKey(key, color)
        return

    # Prints information to the console
    # -> Also writes to a log file in assets
    def log(self, content):
        out_content = f"{self.getSystemTime()} {self.SOURCE_KEY} {content}"
        print(out_content)
        self.writeRuntimeLogs(out_content)
        return out_content
    # -> Also writes to a log file in assets
    def log_error(self, content):
        out_content = f"{self.getSystemTime()} {self.SOURCE_KEY} {clr(content, 'red', attrs=["reverse", "blink"])}"
        print(out_content)
        self.writeRuntimeLogs(out_content)
        return out_content

    # Sets the source key
    def setSourceKey(self, key, color):
        self.SOURCE_KEY = str(clr(f" [{key}] ", color))

    # Sets the source key with a route
    ROUTE_COLOR = 'yellow'
    def setSourceKeyRoute(self, key, route, color):
        self.SOURCE_KEY = str(clr(f" [{key}/{clr(route, self.ROUTE_COLOR)}", color) + clr("] ", color))

    # Gets the current system time
    def getSystemTime(self):
        return clr(f"[{datetime.now().strftime("%H:%M:%S")}] ", 'light_grey')

    # Clears any information in runtime logs
    def resetRuntimeLogs(self):
        # Access runtime logs, delete all content
        with open(self.RUNTIME_LOG_FILEPATH, 'w') as file:
            file.write('')
        return

    # Writes to runtime logs
    def writeRuntimeLogs(self, content):
        # Access runtime logs, delete all content
        with open(self.RUNTIME_LOG_FILEPATH, 'a') as file:
            file.write(f"{content}\n")
        return

    # Hold formatting constants
    FORMAT_DIVIDER = "===================="
    def start_divide(self, title):
        self.log(" ")
        self.log(clr(f"{self.FORMAT_DIVIDER} {title} {self.FORMAT_DIVIDER}", 'green'))

    def end_divide(self, title):
        self.log(clr(f"{self.FORMAT_DIVIDER} {title} {self.FORMAT_DIVIDER}", 'red'))
        self.log(" ")

    def error_divide(self, title):
        self.log(clr(f"{self.FORMAT_DIVIDER} {title} {self.FORMAT_DIVIDER}", 'red', attrs=["reverse", "blink"]))
        self.log(" ")