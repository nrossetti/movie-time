from datetime import datetime

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