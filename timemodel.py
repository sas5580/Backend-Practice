from typing import Dict

class Time:
    def __init__(self, hour: int, minute: int):
        if not (0 <= minute < 60 and 0 <= hour < 24):
            raise ValueError('Invalid hour or minute value')
        self.hour = hour
        self.minute = minute

    @classmethod
    def fromdict(cls, time_dict: Dict[str, int]):
        return cls(time_dict['hour'], time_dict['minute'])

    def in_seconds(self):
        return self.hour*60 + self.minute

    def __str__(self):
        return '%02d:%02d' % (self.hour, self.minute)