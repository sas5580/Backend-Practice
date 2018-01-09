from dao import DAO

from event import Event

class ScheduleDAO(DAO):
    def get(self, owner):
        return self._get_one_by_params('schedule', {'owner': owner})

    def update(self, schedule):
        return self._update('schedule',{'owner': schedule.owner}, {'events': list(map(str, schedule.events))}, True)
