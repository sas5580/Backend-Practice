from copy import deepcopy

from dao import DAO

class EventDAO(DAO):
    def get(self, event_name):
        return self._get_one_by_params('event', {'name': event_name})

    def get_by_id(self, id_str):
        return self._get_by_id('event', id_str)

    def create(self, event):
        return self._save_one('event', deepcopy(vars(event)))

    def update(self, event):
        return self._update('event', {'name': event.name}, vars(event))

    def delete(self, event_name):
        return self._delete('event', {'name': event_name})
