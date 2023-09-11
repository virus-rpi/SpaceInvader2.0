from typing import NamedTuple


class ServerData(NamedTuple):
    online_players: bool
    max_players: bool
    version: bool
    motd: bool
    plugins: bool
    server_type: bool
    whitelist: bool
    ping: bool
    last_scanned: bool
    last_online: bool
    geo: bool
    rcon: bool
    shodan: bool


standard_data = ServerData(online_players=True, max_players=True, version=True, motd=True, plugins=False,
                           server_type=False, whitelist=False, ping=True, last_scanned=True, last_online=True,
                           geo=False, rcon=False, shodan=False
                           )


class ServerReconnaissance:
    def __init__(self, db=None, config=None):
        self.db = db
        self.config = config

    def investigate(self, server_id=None, server_ip=None, server_port=None, update_db=False, data: ServerData = None):
        if data is None:
            data = standard_data
        if server_id is not None and server_ip is not None:
            raise ValueError("Only one of id or ip should be provided, not both.")
        if server_id is None and server_ip is None:
            raise ValueError("Either id or ip must be provided.")
        if server_id is not None and server_port is not None:
            raise ValueError("Port should not be provided if id is provided.")
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")

        if server_id is not None:
            return self.investigate_by_id(server_id, update_db, data)
        elif server_ip is not None:
            if server_port is not None:
                return self.investigate_by_ip(server_ip, server_port, update_db, data)
            else:
                raise ValueError("Port must be provided if ip is provided.")
        return None

    def investigate_by_id(self, server_id, update_db=False, data: ServerData = None):
        if data is None:
            data = standard_data
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")
        ip = self.db.find({"_id": server_id})[0]["ip"]
        port = self.db.find({"_id": server_id})[0]["port"]
        return self.investigate_by_ip(ip, port, update_db, data)

    def investigate_all(self, update_db=True, data: ServerData = None, celery=False):
        if celery:
            if 'Celery' not in self.config['features']:
                raise ValueError("Celery must be enabled in config to use this function.")
        if data is None:
            data = standard_data
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")
        results = []
        if celery:
            pass  # send task to celery
        else:
            for server in self.db.find({}):
                results.append(self.investigate_by_ip(server["ip"], server["port"], update_db, data))
        return results

    def investigate_by_ip(self, server_ip, server_port=25565, update_db=False, data: ServerData = None):
        if data is None:
            data = standard_data
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")

        server_data = {"ip": server_ip, "port": server_port, "online": True if True else False, "online_players": None,
                       "max_players": None, "version": None, "motd": None, "plugins": None, "server_type": None,
                       "whitelist": None, "ping": None, "last_scanned": None, "last_online": None, "geo": None,
                       "rcon": None, "shodan": None}

        if data.online_players:
            server_data["online_players"] = None
        if data.max_players:
            server_data["max_players"] = None
        if data.version:
            server_data["version"] = None
        if data.motd:
            server_data["motd"] = None
        if data.plugins:
            server_data["plugins"] = None
        if data.server_type:
            server_data["server_type"] = None
        if data.whitelist:
            server_data["whitelist"] = None
        if data.ping:
            server_data["ping"] = None
        if data.last_scanned:
            server_data["last_scanned"] = None
        if data.last_online:
            server_data["last_online"] = None
        if data.geo:
            server_data["geo"] = None
        if data.rcon:
            server_data["rcon"] = None
        if data.shodan:
            server_data["shodan"] = None

        return server_data
