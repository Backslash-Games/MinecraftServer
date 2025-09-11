import os

import src.discord_bot.message_stream as stream

import src.tools.console_formatting as cf
import src.tools.directory_manager as dm
import src.tools.file_manager as fm
import src.tools.time_format as tf
from src.commands import BACKUP_DIRECTORY_ALLOWED_LENGTH, TRIM_BACKUP_DIRECTORY

# Define final variables
CWD = os.getcwd()
KEY = "BACKUP"
SERVER_WORLD_PATH = "/server/world"
# Define Logger
source = cf.Console(KEY, "yellow")



# Backup a folder
world_directory = dm.DirectoryManager(KEY, SERVER_WORLD_PATH)
backup_out = world_directory.backup()
source.log(f"Backup finished with response **{backup_out}**")

# Output response to server
stream.send(f"Backup method finished with response **{backup_out}**")



# Trims the backup directory
def trim_earliest(directory, contents):
    time_format_list = []
    for file in contents:
        trimmed_file = file.replace("backup_", "")
        trimmed_file = trimmed_file.replace(".zip", "")
        time_format_list.append(trimmed_file)
    target_time = tf.Time.get_earliest(time_format_list)
    source.log(target_time)
    backup_file_name = f"backup_{tf.Time.to_time_format(target_time)}.zip"
    source.log(backup_file_name)
    fm.FileManager.delete_file(directory.get_directory_root(), backup_file_name)

if TRIM_BACKUP_DIRECTORY:
    # Trim directory until there are only 10 entries
    backup_directory = dm.DirectoryManager(KEY, backup_out[0:backup_out.rfind("/")].replace(CWD, ''))
    directory_list = backup_directory.get_contents()
    # Check length
    while len(directory_list) > BACKUP_DIRECTORY_ALLOWED_LENGTH:
        trim_earliest(backup_directory, directory_list)
        directory_list = backup_directory.get_contents()