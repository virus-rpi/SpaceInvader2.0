import logging


class ServerScanner:
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def scan(self):
        if self.config["scanner"] == "Qubo Scanner":
            self.qubo_scan()
        elif self.config["scanner"] == "Masscan":
            self.masscan_scan()
        else:
            logging.error("Invalid scanner selected")

    def qubo_scan(self):
        pass

    def masscan_scan(self):
        pass
