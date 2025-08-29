import os
import sys
from termcolor import colored as clr

sys.path.append(os.getcwd() + "/src/tools")
import console_formatting as cf

class PacketManager:
    CWD = os.getcwd()
    packet_directory = ""

    source = cf.Console("PACKET_MANAGER", 'magenta')

    def __init__(self, route, directory):
        # Update the source for proper logging
        self.source.setSourceKeyRoute("PACKAGE_MANAGER", route, 'magenta')
        # Define the packet directory
        self.packet_directory = self.CWD + directory
        # Let console know that we have set up
        self.source.log(f"New packet manager set up with directory {clr(directory, 'yellow')}")

    # Sends packet information (as json) to a pre-defined file name
    SEND_FILE_NAME = "/send.json"
    def send(self):
        target_file = self.packet_directory + self.SEND_FILE_NAME
        self.source.log(f"Sending packet to {target_file}")

    # Receives packet information (as json) to a pre-defined file name
    RECEIVE_FILE_NAME = "/receive.json"
    def receive(self):
        return