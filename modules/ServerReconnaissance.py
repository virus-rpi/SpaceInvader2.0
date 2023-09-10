class ServerReconnaissance:
    def __init__(self, db=None):
        self.db = db

    def investigate(self, server_id=None, server_ip=None, server_port=None, update_db=False):
        if server_id is not None and server_ip is not None:
            raise ValueError("Only one of id or ip should be provided, not both.")
        if server_id is None and server_ip is None:
            raise ValueError("Either id or ip must be provided.")
        if server_id is not None and server_port is not None:
            raise ValueError("Port should not be provided if id is provided.")
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")

        if server_id is not None:
            return self._investigate_by_id(server_id, update_db)
        elif server_ip is not None:
            if server_port is not None:
                return self._investigate_by_ip(server_ip, server_port, update_db)
            else:
                raise ValueError("Port must be provided if ip is provided.")
        return None

    def _investigate_by_id(self, server_id, update_db=False):
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")
        ip = self.db.find({"_id": server_id})[0]["ip"]
        port = self.db.find({"_id": server_id})[0]["port"]
        return self._investigate_by_ip(ip, port)

    def _investigate_by_ip(self, server_ip, server_port=25565, update_db=False):
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")
        return None

    def investigate_all(self, update_db=False):
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")
        results = []
        for server in self.db.find({}):
            results.append(self._investigate_by_ip(server["ip"], server["port"], update_db))
        return results
