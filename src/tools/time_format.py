from datetime import datetime

from src.tools import TIME_FORMAT_LENGTH, static_source


# Full of static methods to help with formatting time
class Time:
    @staticmethod
    # Returns a string in the local time format
    # time_format is defined as "d%Y%m%dt%H%M%S"
    def get_format_now():
        return Time.to_time_format(datetime.now())


    @staticmethod
    # Gets the earliest entry from a list of time formats
    def get_earliest(time_format_list):
        dt_now = datetime.now()
        # Return if there are no entries in time format list
        if len(time_format_list) <= 0:
            static_source.log_error("Time format list received with 0 entries")
            return dt_now
        # Convert all time formats into date time
        dt_list = []
        for time_format in time_format_list:
            dt_list.append(Time.to_datetime(time_format))

        # Return if there are no entries in dt list
        if len(dt_list) <= 0:
            static_source.log_error("Date Time list received with 0 entries")
            return dt_now

        # Find smallest
        dt_smallest = dt_now
        for dt in dt_list:
            if dt < dt_smallest:
                dt_smallest = dt

        # Return the smallest
        return dt_smallest


    @staticmethod
    # Checks if format string is the correct length
    def is_correct_length(time_format):
        out_bool = len(time_format) == TIME_FORMAT_LENGTH
        if not out_bool:
            static_source.log_error(f"Time format length is incorrect size, check input {time_format}")
        return out_bool

    @staticmethod
    # Converts time format to list
    def to_list(time_format):
        # Check if format is correct
        if not Time.is_correct_length(time_format):
            return []

        # Processing message
        static_source.log(f"Processing string: {time_format}")
        # Remove readable formatting
        time_format = time_format.replace('d', '')
        time_format = time_format.replace('t', '')
        static_source.log(f"Removed Readable formatting: {time_format}")

        # Split message into chunks
        time_out = [int(time_format[0:4]), int(time_format[4:6]), int(time_format[6:8]), int(time_format[8:10]), int(time_format[10:12]),
                    int(time_format[12:])]

        # Output processing
        static_source.log(f"Processing done: {time_out}")
        return time_out

    @staticmethod
    # Converts time format to date time
    def to_datetime(time_format):
        # Check if format is correct
        if not Time.is_correct_length(time_format):
            return datetime.now()

        # Create a list
        time_list = Time.to_list(time_format)

        # Convert list into datetime
        dt_out = datetime(time_list[0], time_list[1], time_list[2], time_list[3], time_list[4], time_list[5])
        return dt_out

    @staticmethod
    # Datetime to time format
    def to_time_format(date_time):
        if not isinstance(date_time, datetime):
            static_source.log_error(f"File given is not {type(datetime)} but instead {type(date_time)}")
            return ""
        return date_time.strftime("d%Y%m%dt%H%M%S")