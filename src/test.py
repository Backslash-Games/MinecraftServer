import src.tools.console_formatting as cf
import src.tools.time_format as tf
from src import TIME_FORMAT_TEST_STRING, TIME_FORMAT_TEST_LIST, RUN_TEST_TIME

# Initialize console
source = cf.Console("TEST", 'cyan')

# ========== TIME TESTS ==========
if RUN_TEST_TIME:
    source.log(f"Current Time: {tf.Time.get_format_now()}")
    source.log(tf.Time.to_datetime(TIME_FORMAT_TEST_STRING))
    source.log(tf.Time.get_earliest(TIME_FORMAT_TEST_LIST))