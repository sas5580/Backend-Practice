from copy import deepcopy
from bson.objectid import ObjectId

from dao import DAO

class ScheduleDAO(DAO):
    def get(self, owner=None):
        return self._get_by_params('schedule', {'owner': owner} if owner else {})

    def get_by_id(self, s_id):
        return self._get_by_id('schedule', s_id)

    def create(self, sched):
        return self._save_one('schedule', deepcopy(vars(sched)))

    def update(self, sched):
        return self._update('schedule', {'_id': ObjectId(sched.id)}, {'events': sched.events})

    def delete(self, sched):
        return self._delete('schedule', {'_id': ObjectId(sched.id)})
