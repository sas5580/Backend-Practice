from datetime import datetime

from validations import validate_OId

DAYS = set(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))

def read_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

def validate_times(from_time, to_time):
    from_time, to_time = read_time(from_time), read_time(to_time)
    return from_time <= to_time

def validate_days(days):
    return set(days).issubset(DAYS)

def validate_put(e_id, data):
    res = validate_OId(e_id)
    if 'days' in data: res &= validate_days(data['days'])
    if 'from_time' in data: res &= read_time(data['from_time']) is not None
    if 'to_time' in data: res &= read_time(data['to_time']) is not None
    if not res: raise ValueError('Invalid Event PUT payload')

def validate_post(data):
    if not('name' in data and validate_days(data['days']) and validate_times(data['from_time'], data['to_time'])):
        raise ValueError('Invalid Event POST payload')
