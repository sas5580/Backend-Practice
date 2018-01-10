from dao import DAO

from event import Event

class ScheduleDAO(DAO):
    def get(self, owner):
        res = self._get_by_params('schedule', {'owner': owner})
        return res[0] if len(res) > 0 else None

    def update(self, schedule):
        return self._update('schedule',{'owner': schedule.owner}, {'events': schedule.events}, True)
