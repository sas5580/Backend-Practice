from dao import DAO

class ScheduleDAO(DAO):
    def get(self, owner):
        return self._get_by_params('schedule', {'owner': owner})

    def update(self, schedule):
        return self._update('schedule',{'owner': schedule.owner}, {'events': [e.name for e in schedule.events]})