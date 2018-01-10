from copy import deepcopy
from bson.objectid import ObjectId

from dao import DAO

class EventDAO(DAO):
    def get(self, event_name=None):
        return self._get_by_params('event', {'name': event_name} if event_name else {})

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

    def count_id(self, e_id):
        return self._count({'_id': ObjectId(e_id)})
