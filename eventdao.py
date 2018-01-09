from dao import DAO

class EventDAO(DAO):
    def get(self, event_name):
        return self._get_one_by_params('event', {'name': event_name})

    def get_by_id(self, id_str):
        return self._get_by_id('event', id_str)

    def create(self, event):
        return self._save_one('event', event.serialize())

    def update(self, event):
        return self._update('event', {'name': event.name}, event.serialize())

    def delete(self, event_name):
        return self._delete('event', {'name': event_name})
