from copy import deepcopy
from bson.objectid import ObjectId

from dao import DAO

class ScheduleDAO(DAO):
    def get(self, owner):
        return self._get_by_params('schedule', {'owner': owner} if owner else {})

    def get_by_id(self, s_id):
        return self._get_by_id('schedule', ObjectId(s_id))

    def create(self, sched):
        return self._save_one('schedule', deepcopy(vars(sched)))

    def update(self, sched):
        return self._update('schedule',{'owner': sched.owner}, {'events': sched.events}, True)

        
