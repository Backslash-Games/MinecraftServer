# Storage backup is used to backup files on a drive in the unit that are decoupled from the bigger system

# Import basic
import os
import shutil
import sys

# Import tools
from src.tools import json_manager as jm
from src.tools import directory_manager as dm
from src.tools import file_manager as fm

from src.tools import console_formatting as cf

# Create a global console
global source
source = cf.Console("STORAGE BACKUP", "red")

# Hold a reference to backup storage config
CWD = os.getcwd()
SB_CONFIG_PATH = CWD + "/assets/storage/backup_storage.json"

# Create a static class
class Storage_Backup:

    @staticmethod
    # Create a backup of information on the storage path
    def backup_file(path, file_name):
        global source
        source.log(f"Backing up {file_name} on storage")

        # Start by pulling information regarding the backup directory
        backup_path = jm.getJsonValue(SB_CONFIG_PATH, "path")
        source.log(f"Found backup path {backup_path}")

        # Check if output directory exists... DO NOT CREATE LOCATION IF IT DOESNT EXIST
        if not dm.DirectoryManager.is_valid_directory(backup_path):
            source.log_error(f"Backup path {backup_path} does not exist. Please set up value 'path' in {SB_CONFIG_PATH}")
            return "Backup failed"

        # Define input and output
        input_file = f"{path}/{file_name}"
        output_file = f"{backup_path}/{file_name}"
        # Temp FM fix later
        temp_fm = fm.FileManager("Storage Backup")

        # Check if input file exists
        if not temp_fm.exists(input_file):
            source.log_error(f"Input file {input_file} does not exist! Returning early")
            return "Backup failed"

        # Copy file into path
        shutil.copyfile(input_file, output_file)
        source.log("Successfully backed up file")

        return f"File successfully backed up to additional drive.\nDrive Path: **{backup_path}**\nFile Name: **{file_name}**"