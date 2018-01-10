from copy import deepcopy
from bson.objectid import ObjectId

from dao import DAO

class EventDAO(DAO):
    def get_by_name(self, event_name):
        res = self._get_by_params('event', {'name': event_name})
        return res[0] if len(res) > 0 else None

    def get_by_id(self, id_str):
        return self._get_by_id('event', id_str)

    def get_all(self):
        return self._get_by_params('event', {})

    def create(self, event):
        return self._save_one('event', deepcopy(vars(event)))

    def update(self, event):
        return self._update('event', {'name': event.name}, vars(event))

    def delete(self, e_id):
        return self._delete('event', {'_id': ObjectId(e_id)})
