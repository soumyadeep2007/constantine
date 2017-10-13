import logging

import log_messages
from commons import Commons


# noinspection PyUnresolvedReferences,PyStatementEffect
class Client (process):
    def setup(self, olympus):
        self._id = 1  # todo
        self._pending_requests = {}
        self._olympus = olympus
        # todo

    def _update_config(self):
        self._current_config = self._olympus.fetchConfig()
        output(log_messages.CONFIG_FETCHED)

    def _create_operation(self):
        pass  # return an operation with given parameters

    def _issue_request(self, operation):
        request_message = self._create_request(operation, is_retry=False)
        self._pending_requests[operation['id']] = request_message
        send(('request', request_message), to=self._current_config['head'])
        -- result
        if await(received(('result'), message, pid), from_=self._current_config['replicas']):
            output(log_messages.RESULT_RECEIVED, pid)
        elif timeout(self._current_config["client_timeout"]):
            _handle_request_timeout(request_message)

    def _create_request(self, operation, is_retry):
        request_message = {
            'content': {
                'is_retry': is_retry,
                'operation': operation
            }
        }
        request_message['signed_content'] = Commons.sign(request_message['content'], self._private_key)
        return request_message

    # On receipt of a keys message
    def receive(self, msg=('keys', message), from_=self._olympus):
        if not Commons.is_valid_signature(message, self._public_key):
            output(log_messages.INVALID_SIGNATURE, from_, level=logging.ERROR)
            return
        self._private_key = message['private_key']
        self._public_keys = message['public_keys']

    # On receipt of a result message from a replica
    def receive(self, msg=('result', message), from_=self._current_config['replicas']):
        if not Commons.is_valid_signature(message, self._public_keys[from_["id"]]):
            output(log_messages.INVALID_SIGNATURE, level=logging.ERROR)
            return
        if message['content']['operation']['id'] not in self._pending_requests:
            return
        if Commons.is_valid_result(message, self._current_config['replicas'], self._public_keys):
            self._pending_requests.pop(message['content']['operation'])
            self._process_result(message['content']['operation'], message['content']['result'])
        else:
            self._retry_request(message)

    # On receipt of an error message from a replica
    def receive(self, msg=('error', message), from_=self._current_config['replicas']):
        if not Commons.is_valid_signature(message, self._public_keys[from_["id"]]):
            return
        self._retry_request(message)

    def _process_result(self, operation, result):
        pass

    def _retry_request(self, message):
        message['content']['is_retry'] = True
        message['signed_content'] = Commons.sign(message['content'], self._private_key)
        for replica in self._current_config['replicas']:
            pass  # send here to every replica
        # todo

    def _handle_request_timeout(self, message):
        self._retry_request(message)

    def __hash__(self):
        return hash((self._id))

    def __eq__(self, other):
        return self._id == other._id
