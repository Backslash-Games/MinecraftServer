import os
import sys
import time

import src.tools.console_formatting as cf
import src.tools.file_manager as file_manager
import src.server_tools.local_packet.local_packet_manager as lpm

CWD = os.getcwd()

QUEUE_FILEPATH = CWD + "/assets/server/cmd_queue.txt"
PACKET_PATH = CWD + "/server/sh"

source = cf.Console("MINECRAFT_COMMANDS", 'light_yellow')

# Set up the file manager
fm = file_manager.FileManager("MINECRAFT_COMMANDS")
fm.source.set_suppression(True)
# Set up the packet manager
packet = lpm.PacketManager("MINECRAFT_COMMANDS", PACKET_PATH)


# Check if a command is waiting to be sent
def on_update():
    # Check if file exists
    if not fm.exists(QUEUE_FILEPATH):
        return

    # Read file and perform operations
    command_queue = fm.read_file(QUEUE_FILEPATH).split("\n")
    command_queue.remove('')

    # Send the command
    if len(command_queue) > 0:
        source.log(f"We got a command to send {command_queue[0]}")
        packet.send()

# Add a command to be sent
def add_command(content):
    # Check if file exists
    fm.append_file(QUEUE_FILEPATH, content)