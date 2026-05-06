# Context helper untuk menyimpan state antar request

class UserContext:
    def __init__(self):
        self._store = {}

    def set(self, user_id, key, value):
        uid = str(user_id)
        if uid not in self._store:
            self._store[uid] = {}
        self._store[uid][key] = value

    def get(self, user_id, key, default=None):
        uid = str(user_id)
        return self._store.get(uid, {}).get(key, default)

    def clear(self, user_id):
        uid = str(user_id)
        self._store.pop(uid, None)


user_context = UserContext()
