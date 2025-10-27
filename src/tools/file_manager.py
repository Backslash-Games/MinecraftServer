import os
from termcolor import colored as clr

# ========== TOOL SETUP ==========
from . import console_formatting as cf
from ..server_tools.log.console_print import source

CWD = os.getcwd()
# MAIN GOAL - Quickly pull and push information to files stored in /assets
class FileManager:
    # define root source
    KEY = "FILE_MANAGEMENT"
    COLOR = "light_grey"

    route = "UNKNOWN"
    source = cf.Console(KEY, COLOR)
    CWD = os.getcwd()

    def __init__(self, route):
        self.set_route(route)
        return

    # Updates the source key
    def update_source_key(self):
        self.source.setSourceKeyRoute(self.KEY, self.route, self.COLOR)

    # Sets the route
    def set_route(self, route):
        self.route = route
        self.update_source_key()

    # If file exists return all information contained
    def read_file(self, path):
        if not self.exists(path):
            self.source.log_error(f"Could not complete readFile({path})")
            return ''
        with open(path, 'r') as file:
            return file.read()

    # Writes to file
    def write_file(self, path, content):
        return

    # Appends content to a file
    def append_file(self, path, content):
        # Check if file exists
        if not self.exists(path):
            self.source.log(f"File at path '{clr(path, 'yellow')}' {clr("does not exist", 'red')}... Creating now")

        # Open file
        with open(path, 'a') as file:
            file.write(content + "\n")

    # Check if file at path exists
    def exists(self, path):
        # Check if the file exists
        if os.path.exists(path):
            self.source.log(f"File at path '{clr(path, 'yellow')}' {clr("exists", 'green')}")
            return True
        self.source.log(f"File at path '{clr(path, 'yellow')}' {clr("does not exist", 'red')}")
        return False

    @staticmethod
    # Deletes a file
    def delete_file(path, file_name):
        static_source = cf.Console("STATIC::TOOLS", 'red')
        static_source.set_suppression(False)

        # Delete the file
        target = f"{path}/{file_name}"

        # Check if the file exists
        if os.path.exists(path):
            static_source.log(f"File at path '{clr(target, 'yellow')}' {clr("exists", 'green')}")
        else:
            static_source.log_error(f"Couldn't find file at path {target}")
            return

        os.remove(target)
        static_source.log_warning(f"DELETING FILE {target}")

    @staticmethod
    # Gets the file size
    def get_file_size(path, file_name):
        static_source = cf.Console("STATIC::TOOLS", 'red')
        static_source.set_suppression(False)

        # Get the target
        target = f"{path}/{file_name}"

        # Check if the file exists
        if os.path.exists(path):
            static_source.log(f"File at path '{clr(target, 'yellow')}' {clr("exists", 'green')}")
        else:
            static_source.log_error(f"Couldn't find file at path {target}")
            return 0

        target_bytes = os.path.getsize(target)
        static_source.log(f"File at path '{clr(target, 'yellow')}' is size {clr(target_bytes, 'green')}")
        return target_bytes

    @staticmethod
    # Splits file name and path
    def split_file_path(file_path):
        # Set source
        static_source = cf.Console("STATIC::TOOLS", 'red')
        static_source.set_suppression(False)
        # Do calculations
        split_index = file_path.rfind("/") + 1;
        path = file_path[0:split_index - 1]
        file_name = file_path[split_index:]
        # Write to log
        static_source.log(f"Split file path into PATH: {path} and FILE NAME: {file_name}")
        return [path, file_name]