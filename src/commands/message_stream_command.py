# Handles different debug components for the message stream

from src.tools import console_formatting as cf
from src.discord_bot import message_stream as stream


# Set source
source = cf.Console("MESSAGE STREAM DEBUG", "cyan")
# Pull all arguments
cmd_args = stream.get_args()
source.log(f"Arguments pulled: {cmd_args}")

# All Possible Branches
# -> Requeues the message stream
def queueMessageStream():
    source.log("Setting queued to true")
    stream.setQueued(True)


# Check what command to run
if cmd_args[0] == "queue":
    queueMessageStream()