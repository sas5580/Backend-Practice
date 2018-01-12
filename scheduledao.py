from copy import deepcopy
from bson.objectid import ObjectId

from dao import DAO

class ScheduleDAO(DAO):
    def get(self, owner=None):
        return self._get_by_params('schedule', {'owner': owner} if owner else {})

    def get_by_id(self, s_id):
        return self._get_by_id('schedule', s_id)

    def events_empty(self, s_id):
        return not self._get_by_params('schedule', {'_id': ObjectId(s_id), 'events': {'$ne': []}})

    def create(self, sched):
        return self._save_one('schedule', deepcopy(vars(sched)))

    def add_event(self, s_id, e_id):
        return self._addToSet('schedule', {'_id': ObjectId(s_id)}, {'events': e_id})

    def remove_event(self, s_id, e_id):
        return self._pull('schedule', {'_id': ObjectId(s_id)}, {'events': e_id})

    def delete(self, s_id):
        return self._delete('schedule', {'_id': ObjectId(s_id)})
