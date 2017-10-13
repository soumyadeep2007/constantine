class Client (process):
    def update_config(self, olympus):
        self._current_config = olympus.fetchConfig()

    def on_keys_message(self, message):
        self._private_key = message.private_key
        self._public_keys = message.public_keys
