# Returns server logs
import os
import src.discord_bot.message_stream as stream

CWD = os.getcwd()
stream.send("Returning logs", f"{CWD}/assets/runtime.log")