from datetime import datetime

DAYS = set(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))

def read_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

def validate_times(from_time, to_time):
    from_time, to_time = read_time(from_time), read_time(to_time)
    return from_time <= to_time

def validate_days(days):
    return set(days).issubset(DAYS)
        
