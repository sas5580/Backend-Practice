from dao import DAO

class EventDAO(DAO):
    def get(self, event_name):
        return self._get_by_params('event', {'name': event_name}).next()

    def create(self, event):
        return self._save('event', event.serialize())

    def update(self, event):
        return self._update('event', {'name': event.name}, event.serialize())

    def delete(self, event_name):
        return self._delete('event', {'name': event_name})
