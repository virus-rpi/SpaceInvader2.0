from typing import NamedTuple
from mcstatus import JavaServer


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

    def investigate(self, server_id: int = None, server_ip: str = None, server_port: int = None,
                    update_db: bool = False,
                    data: ServerData = None):
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
        if server_id is not None and self.db is None:
            raise ValueError("Database must be provided if id is provided.")

        if server_id is not None:
            return self._investigate_by_id(server_id, update_db, data)
        elif server_ip is not None:
            if server_port is not None:
                return self._investigate_by_ip(server_ip, server_port, update_db, data)
            else:
                raise ValueError("Port must be provided if ip is provided.")
        return None

    def _investigate_by_id(self, server_id: int, update_db: bool = False, data: ServerData = None):
        if data is None:
            data = standard_data
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")
        ip = self.db.find({"_id": server_id})[0]["ip"]
        port = self.db.find({"_id": server_id})[0]["port"]
        return self._investigate_by_ip(ip, port, update_db, data)

    def investigate_all(self, update_db: bool = True, data: ServerData = None, celery: bool = False):
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
                results.append(self._investigate_by_ip(server["ip"], server["port"], update_db, data))
        return results

    def _investigate_by_ip(self, server_ip: str, server_port: int = 25565, update_db: bool = False,
                           data: ServerData = None):
        if data is None:
            data = standard_data
        if update_db and self.db is None:
            raise ValueError("Database must be provided if update_db is True.")

        server = Server(server_ip, server_port)

        server.update(data)

        server_data = dict(server)

        if update_db:
            pass  # update db

        return server_data


class Server:
    def __init__(self, ip: str, port: int = 25565):
        self.ip = ip
        self.port = port
        self.online = None
        self.online_players = None
        self.max_players = None
        self.version = None
        self.motd = None
        self.plugins = None
        self.server_type = None
        self.whitelist = None
        self.ping = None
        self.last_scanned = None
        self.last_online = None
        self.geo = None
        self.rcon = None
        self.shodan = None
        self.query_enabled = None

    def __str__(self) -> str:
        return f"Server({self.ip}:{self.port})"

    def __repr__(self) -> str:
        fields = [
            "online", "online_players", "max_players", "version", "motd", "plugins",
            "server_type", "whitelist", "ping", "last_scanned", "last_online", "geo", "rcon", "shodan"
        ]
        attributes = ', '.join([f"{field}={getattr(self, field)}" for field in fields if getattr(self, field) is not None])
        return f"Server({self.ip}:{self.port}): {attributes}"

    def __eq__(self, other) -> bool:
        return self.ip == other.ip and self.port == other.port

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.ip, self.port))

    def __bool__(self) -> bool:
        return self.online

    def __int__(self) -> int:
        return self.ping

    def __iter__(self) -> iter:
        fields = [
            "ip", "port", "online", "online_players", "max_players", "version",
            "motd", "plugins", "server_type", "whitelist", "ping",
            "last_scanned", "last_online", "geo", "rcon", "shodan"
        ]
        for field in fields:
            value = getattr(self, field)
            if value is not None:
                yield field, value

    def _get_data(self, data: ServerData):  # TODO: test this function and fix if necessary
        offline_errors = (ConnectionError or ConnectionResetError or ConnectionRefusedError or TimeoutError)

        server = JavaServer.lookup(f"{self.ip}:{self.port}")
        server_data = None

        try:
            if (data.plugins or data.server_type) and self.query_enabled is not False:
                server_data = server.query()
                self.query_enabled = True
            else:
                raise offline_errors
        except offline_errors:
            try:
                server_data = server.status()
                self.query_enabled = False
            except offline_errors:
                pass

        return server_data

    def update(self, data: ServerData) -> None:  # TODO: add the rest of the data and fix errors with different data structures between status and query
        server_data = self._get_data(data)

        self.online = True if server_data is not None else False

        if self.online:
            self.online_players = server_data.players.online if data.online_players else None
            self.max_players = server_data.players.max if data.max_players else None
            self.version = server_data.version.name if data.version else None
            self.motd = server_data.description if data.motd else None
            self.ping = round(server_data.latency, 2) if data.ping else None
