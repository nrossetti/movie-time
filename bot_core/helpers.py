from datetime import datetime, timedelta
from enum import Enum
import pytz, re
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
    """
    Rounds a UNIX timestamp to the next quarter-hour mark.
    """
    if not isinstance(timestamp, int):
        raise ValueError("Timestamp must be an integer")
    time = datetime.fromtimestamp(timestamp, tz=pytz.utc)
    if time.minute % 15 == 0:
        # If the time is already at a quarter-hour mark, don't round it
        return timestamp
    minutes_to_next_quarter_hour = 15 - time.minute % 15
    rounded_time = time + timedelta(minutes=minutes_to_next_quarter_hour)
    rounded_time = rounded_time.replace(second=0, microsecond=0)
    return int(rounded_time.timestamp())

def parse_start_time(time_string: str, timezone_enum: TimeZones, date_str=None):
    """
    parse start time into a unix timestamp
    """
    local_tz = pytz.timezone(timezone_enum.value)
    if date_str:
        try:
            date = parse_date(date_str)
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")
    else:
        date = datetime.now(tz=local_tz).date()

    for fmt in ['%H:%M', '%I %p', '%I%p', '%I:%M %p', '%I:%M%p']:
        try:
            parsed_time = datetime.strptime(time_string, fmt)
            local_datetime = local_tz.localize(datetime.combine(date, parsed_time.time()))
            utc_datetime = local_datetime.astimezone(pytz.utc)
            return int(utc_datetime.timestamp())
        except ValueError:
            continue
    raise ValueError(f"Time {time_string} is not in the expected format")


def parse_date(date_str):
    """
    parse date string
    """
    current_year = datetime.now().year
    match = re.match(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", date_str)
    if match:
        month, day, year = match.groups()
        if year:
            year = int(year)
            if year < 100:
                year += 2000
        else:
            year = current_year
        return datetime(year, int(month), int(day)).date()
    raise ValueError("Invalid date format")