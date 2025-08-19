# This code will do NOTHING but download the server if it is missing
import subprocess
import os
import sys


# Set constants
SERVER_INSTALL_CONFIG_PATH = os.getcwd() + "/config/server-install-url.txt"
SERVER_DIRECTORY = os.getcwd() + "/server"
SERVER_PATH = SERVER_DIRECTORY + "/server.jar"
EULA_PATH = SERVER_DIRECTORY + "/eula.txt"

REINSTALL_COMMAND = "--force-reinstall"


# Create EULA
def CreateEULA():
    # Check if EULA already exists
    if os.path.exists(EULA_PATH):
        return
    # Create a new file
    e_file = open(EULA_PATH, 'w')
    e_file.write("eula=true")
    e_file.close()


# Check if the server already exists
argument_count = len(sys.argv)
if os.path.isdir(SERVER_DIRECTORY) and ((argument_count > 1 and sys.argv[1] != REINSTALL_COMMAND) or argument_count == 1):
    print("server-setup.py --> Server already exists, skipping install... to force reinstall use " + str(REINSTALL_COMMAND))
    CreateEULA()
    sys.exit(0)
elif os.path.isdir(SERVER_DIRECTORY) and argument_count > 1 and sys.argv[1] == REINSTALL_COMMAND:
    # Destroy the server
    response = subprocess.check_output(["rm", "-r", SERVER_DIRECTORY], text=True)
    print(response)



# Pull the URL
url_file = open(SERVER_INSTALL_CONFIG_PATH, 'r')
url = url_file.read()
url_file.close()



# Install the server
try:
    # Run the download
    response = subprocess.check_output(["wget", "-P", SERVER_DIRECTORY, url], text=True)
    print(response)
    # Create a bypass to EULA
    CreateEULA()

# Error if the server cannot be installed due to the sub process
except subprocess.CalledProcessError as e:
    print(f"server-setup.py --> Failed with return {e.returncode}")