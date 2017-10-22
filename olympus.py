import da


class Olympus(process):
    def initialize_config(self, config):
        self._current_config = {}
        self._public_keys = self.generate_public_keys(config["_clients"], config["t"])
