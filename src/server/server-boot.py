# This code will do NOTHING but start the server
import subprocess
import os

# Define constants
SERVER_INSTALL_CONFIG_PATH = os.getcwd() + "/config/server-install-url.txt"
SERVER_DIRECTORY = os.getcwd() + "/server"
SERVER_PATH = SERVER_DIRECTORY + "/server.jar"


# Ensure the server exists
if os.path.exists(SERVER_PATH):
    # Try to run the server
    try:
        # Run the Server
        response = subprocess.check_output(["java", "-Duser.dir="+SERVER_DIRECTORY, "-jar", SERVER_PATH], text=True)
        print(response)

    # Error if the server cannot be installed due to the sub process
    except subprocess.CalledProcessError as e:
        print(f"server-setup.py --> Failed with return {e.returncode}")