# This code will do NOTHING but start the server
import subprocess
import os
import sys
from termcolor import colored as clr

from src.tools import console_formatting as cf



# Pull working directory
CWD = os.getcwd()
# Set source
source = cf.Console("RUN_JAR", "magenta")



# Define a global process
global java_process

# Run a jar file
def runJar(dir, file_name):
    # Extend current working environment
    jar_path = CWD + dir
    jar_file = jar_path + file_name
    # Check if the path exists
    if not doesJarExist(jar_file):
        source.log(f"Jar '{clr(jar_file, 'yellow')}' could not be executed... Returning early")
        return


    # Try to run the jar file
    try:
        # Run the Server
        source.log(f"Running jar '{clr(jar_file, 'yellow')}'")
        # Set the current directory
        old_dir = os.getcwd()
        os.chdir(jar_path)
        # response = subprocess.check_output(["java", "-Duser.dir=" + jar_path, "-jar", jar_file], text=True)
        java_process = subprocess.check_output(["java", "-jar", jar_file], text=True)

        # source.log(f"Popen data\n{clr(java_process, 'light_blue')}")

    # Error if the server cannot be installed due to the sub process
    except subprocess.CalledProcessError as e:
        source.log(f"Could not run jar '{clr(jar_file, 'yellow')}'")
        source.log(f"Failed with exception {e.returncode}")



    source.log(f"Stopping jar '{clr(jar_file, 'yellow')}'")
    source.log_error("!!!!! JAVA FILE STOPPED !!!!!")
    return

# Check if a jar exists
def doesJarExist(file_path):
    source.log(f"Checking if jar '{file_path}' exists")

    # Check for the jar path
    if os.path.exists(file_path):
        source.log(f"Jar '{clr(file_path, 'yellow')}' {clr('does', 'green')} exist")
        return True

    source.log(f"Jar '{clr(file_path, 'yellow')}' {clr('does not', 'red')} exist")
    return False




# Check for debug arguement
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    source.log(clr("BEFORE", 'green'))
    runJar("/server", "/server.jar")
    source.log(clr("AFTER", 'red'))