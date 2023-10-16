from datetime import datetime, timedelta, timezone
from enum import Enum
import pytz

class TimeZones(Enum):
    UTC = 'UTC'
    EST = 'US/Eastern'
    CST = 'US/Central'
    MST = 'US/Mountain'
    PST = 'US/Pacific'
    KST = 'Asia/Seoul'

def local_to_utc(local_time: datetime, local_timezone) -> datetime:
    if isinstance(local_timezone, TimeZones):
        local_tz_str = local_timezone.value
    else:
        local_tz_str = local_timezone

    local_tz = pytz.timezone(local_tz_str)
    
    if local_time.tzinfo is None:
        local_time = local_tz.localize(local_time)
        
    utc_time = local_time.astimezone(pytz.utc)
    return utc_time

def utc_to_local(utc_time: datetime, local_timezone) -> datetime:
    if isinstance(local_timezone, TimeZones):
        local_tz_str = local_timezone.value
    else:
        local_tz_str = local_timezone

    local_tz = pytz.timezone(local_tz_str)
    
    if utc_time.tzinfo is None:
        utc_time = pytz.utc.localize(utc_time)

    local_time = utc_time.astimezone(local_tz)
    return local_time

def datetime_to_unix(dt: datetime) -> int:
    utc_time = dt.astimezone(pytz.utc)
    return int(utc_time.timestamp())

def round_to_next_quarter_hour(time):
    minutes_to_next_quarter_hour = 15 - time.minute % 15
    rounded_time = time + timedelta(minutes=minutes_to_next_quarter_hour)
    return rounded_time.replace(second=0, microsecond=0)

def parse_start_time(time_string: str):
    formats = ['%H:%M', '%I %p', '%I%p', '%I:%M %p', '%I:%M%p']
    for fmt in formats:
        try:
            parsed_time = datetime.strptime(time_string, fmt)
            return datetime.combine(datetime.today(), parsed_time.time())
        except ValueError:
            pass
    try:
        hour = int(time_string)
        parsed_time = datetime.strptime(str(hour), '%H')
        return datetime.combine(datetime.today(), parsed_time.time())
    except ValueError:
        pass

    raise ValueError(f"Time {time_string} is not in the expected format")