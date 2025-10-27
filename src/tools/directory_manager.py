import os
import shutil

import src.tools.console_formatting as cf
import src.tools.time_format as tf

from termcolor import colored as clr

from src.tools import static_source

class DirectoryManager:
    # define root source
    KEY = "DIRECTORY_MANAGER"
    COLOR = "light_grey"
    CWD = os.getcwd()

    route = "UNKNOWN"
    source = cf.Console(KEY, COLOR)
    directory = "/"


    # Initialization
    def __init__(self, route, path):
        # Setup route
        self.route = route
        self.source.setSourceKeyRoute(self.KEY, self.route, 'yellow')
        # Setup directory
        self.set_directory(path)


    # Backups current directory
    def backup(self, id):
        path = self.get_directory_root()
        self.source.log(f"Backing up {DirectoryManager.string_format(path)} passing to static method")
        return DirectoryManager.backup_target(path, id)


    # Sets the directory
    def set_directory(self, path):
        self.source.log(f"Setting path to {DirectoryManager.string_format(path)}")
        self.directory = path


    # Returns the current directory from root
    def get_directory_root(self):
        path = self.CWD + self.directory
        self.source.log(f"Getting directory root {DirectoryManager.string_format(path)}")
        return path

    # Returns a list of contents of current directory
    def get_contents(self):
        path = self.get_directory_root()
        self.source.log(f"Grabbing contents of {DirectoryManager.string_format(path)}")
        if not DirectoryManager.is_valid_directory(path):
            self.source.log_error(f"Path {path} is invalid")
            return []
        return os.listdir(path)


    @staticmethod
    # Formats path string
    def string_format(directory):
        return clr(f"'{directory}'", 'yellow')

    @staticmethod
    # Creates a directory
    def create_directory(directory):
        # If the directory already exists return early
        if DirectoryManager.is_valid_directory(directory):
            static_source.log_error("Trying to create a directory that already exists... returning early")
            return

        # Create the directory
        static_source.log(f"Created directory {DirectoryManager.string_format(directory)}")
        os.mkdir(directory)

    @staticmethod
    # Returns a boolean
    # If the directory is valid (both exists & is a directory)
    def is_valid_directory(directory):
        return os.path.exists(directory) and os.path.isdir(directory)

    @staticmethod
    # Gets the path of current directory one up
    def get_above_directory(directory):
        # Get the index of the last slash
        last_index = directory.rfind("/")
        sliced_directory = directory[0:last_index]
        static_source.log(f"Returning above directory as {DirectoryManager.string_format(sliced_directory)}")
        return sliced_directory

    @staticmethod
    # Backups a directory
    def backup_target(directory, id):
        # Start Read
        static_source.log(f"Backing up {DirectoryManager.string_format(directory)}")



        # Backup Checks
        # -> Ensure directory exists and is a directory
        if not DirectoryManager.is_valid_directory(directory):
            static_source.log_error("Backup failed - Directory doesn't exist")
            return ""

        # -> Back up directory
        backup_directory = DirectoryManager.get_above_directory(directory)
        backup_directory += "/.backup"
        # --> Check if directory exists - If not then create
        if not DirectoryManager.is_valid_directory(backup_directory):
            static_source.log_warning(f"Backup halted - Backup directory {backup_directory} doesn't exist... Creating now")
            DirectoryManager.create_directory(backup_directory)



        # Backup Logic
        # -> Get current backup name
        time_string = tf.Time.get_format_now()
        backup_name = f"{id}.backup_{time_string}"
        # -> Backup world
        try:
            static_source.log(f"Creating backup at {backup_directory}")
            backup_out = shutil.make_archive(backup_name, 'zip', directory)
            static_source.log(f"Successfully created backup. {backup_out}")
        except OSError as e:
            static_source.log_error(f"Could not create backup -- {e}")
            return ""

        # Move the backup to the backup directory
        move_out = shutil.move(backup_out, backup_directory)
        static_source.log(f"Moved backup to directory {move_out}... Backup was successful!")
        return move_out