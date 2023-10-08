"""
`Session` class that use to store cache information about a login user
"""


class DB:
    def __init__(self) -> None:
        self.db = {}

    def add_client(self, client_id):
        if client_id not in self.db:
            self.db[client_id] = {}
            return self.db[client_id]

    def add_obj(self, client_id, key, value):
        if client_id in self.db:
            client = self.db[client_id]
        else:
            client = self.add_client(client_id)

        client[key] = value

    def delete_session(self, client_id):
        del self.db[client_id]

    def get_session(self, client_id, key):
        client = self.db.get(client_id)
        if client is not None:
            return client.get(key)
        return None
