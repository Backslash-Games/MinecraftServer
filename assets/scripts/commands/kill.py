import os
import sys
from termcolor import colored as clr

CWD = os.getcwd()
sys.path.append(CWD + "/src")

import discord_bot.message_stream as stream

stream.send(clr("kill process", 'red'))