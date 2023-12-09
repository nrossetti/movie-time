from datetime import datetime, timedelta, timezone
import pytz
from enum import Enum
class TimeZones(Enum):
    UTC = 'UTC'
    EST = 'US/Eastern'
    CST = 'US/Central'
    MST = 'US/Mountain'
    PST = 'US/Pacific'
    KST = 'Asia/Seoul'

def local_to_utc_timestamp(local_timestamp: int, local_timezone) -> int:
    """
    Converts a local UNIX timestamp to a UTC UNIX timestamp.
    """
    local_time = datetime.fromtimestamp(local_timestamp, pytz.timezone(local_timezone))
    utc_time = local_time.astimezone(pytz.utc)
    return int(utc_time.timestamp())

def utc_to_local_timestamp(utc_timestamp: int, local_timezone) -> int:
    """
    Converts a UTC UNIX timestamp to a local UNIX timestamp.
    """
    utc_time = datetime.fromtimestamp(utc_timestamp, pytz.utc)
    local_time = utc_time.astimezone(pytz.timezone(local_timezone))
    return int(local_time.timestamp())

def round_to_next_quarter_hour_timestamp(timestamp: int) -> int:
    if not isinstance(timestamp, int):
        raise ValueError("Timestamp must be an integer")
    """
    Rounds a UNIX timestamp to the next quarter-hour mark.
    """
    time = datetime.fromtimestamp(timestamp, tz=pytz.utc)
    if time.minute % 15 == 0:
        # If the time is already at a quarter-hour mark, don't round it
        return timestamp
    minutes_to_next_quarter_hour = 15 - time.minute % 15
    rounded_time = time + timedelta(minutes=minutes_to_next_quarter_hour)
    rounded_time = rounded_time.replace(second=0, microsecond=0)
    return int(rounded_time.timestamp())

def parse_start_time(time_string: str, timezone_enum: TimeZones) -> int:
    local_tz = pytz.timezone(timezone_enum.value)
    today = datetime.now(tz=local_tz).date()  # Get today's date in the local timezone

    print("Today's Date in Local Timezone:", today)  # Debugging

    for fmt in ['%H:%M', '%I %p', '%I%p', '%I:%M %p', '%I:%M%p']:
        try:
            parsed_time = datetime.strptime(time_string, fmt)
            local_datetime = local_tz.localize(datetime.combine(today, parsed_time.time()), is_dst=None)
            print("Local Datetime:", local_datetime)  # Debugging

            utc_datetime = local_datetime.astimezone(pytz.utc)
            print("UTC Datetime:", utc_datetime)  # Debugging

            return int(utc_datetime.timestamp())
        except ValueError:
            continue
    raise ValueError(f"Time {time_string} is not in the expected format")