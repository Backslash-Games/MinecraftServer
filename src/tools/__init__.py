from . import console_formatting, file_manager, json_manager, jar_manager

# Establish static source
static_source = console_formatting.Console("STATIC::TOOLS", 'red')
static_source.set_suppression(False)

# Constants
TIME_FORMAT_LENGTH = 16