# Common messages
INVALID_SIGNATURE = 'A signature mismatch occurred from source:'

# Olympus messages
PARSED_CONFIG = "Parsed config:"
GENERATED_KEYS = 'Generated keys:'
CONFIG_REQUEST_RECEIVED = 'Config request received from client='
CONFIG_SENT = 'Config has been sent to client='

# Client messages
REQUESTING_CONFIG = 'Config requested from Olympus by client='
CONFIG_REQUEST_TIMEOUT = 'Config request timed out...retrying...'
CONFIG_FETCHED = 'The config was fetched from Olympus:'
OPERATION_CREATED = 'The following operation was created:'
REQUEST_MADE = 'A request for an operation was made'
RESULT_SENT = 'A result was sent replica, client='
RESULT_RECEIVED = 'A result was received from replica='
VALID_RESULT_RECEIVED = 'The result received is valid:(result, operation)='
INVALID_RESULT_RECEIVED = 'The result received is invalid:(result, operation)='
OPERATION_RESULT_PAIR = 'The operation result pair is='
REQUEST_TIMEOUT = 'Wait for result timed out for operation='
RETRANSMISSION = 'Retransmitting request to all replicas for operation='
INVALID_REQUEST_SOURCE = 'Request received from invalid source'
ERROR_MESSAGE_RECEIVED = 'An error message was received from replica='

# Replica messages
SENDING_ERROR_MESSAGE = 'Sending error message (client_id, replica_id)'
INVALID_SLOT = 'Shuttle received with invalid request slot, dropping shuttle'
INVALID_ORDER_PROOF_REPLICA_MISSING = 'Invalid order proof because order statement missing for replica (replica_id, self._id)'
INVALID_ORDER_PROOF_REPLICA_SIGNATURE_MISMATCH = 'Invalid order proof because order statement signature mismatch for replica (replica_id, self._id)'
INVALID_ORDER_PROOF_REPLICA_SLOT_MISMATCH = 'Invalid order proof because operation mismatch for replica (replica_id, self._id)'
INVALID_RESULT_PROOF_REPLICA_MISSING = 'Invalid result proof because order statement missing for replica (replica_id, self._id)'
INVALID_RESULT_PROOF_REPLICA_SIGNATURE_MISMATCH = 'Invalid result proof because result statement signature mismatch for replica (replica_id, self._id)'
INVALID_RESULT_PROOF_REPLICA_HASH_MISMATCH = 'Invalid result proof because hash mismatch for replica (replica_id, self._id)'
INVALID_CHECKPOINT_PROOF_REPLICA_MISSING = 'Invalid checkpoint proof because checkpoint statement missing for replica (replica_id, self._id)'
INVALID_CHECKPOINT_PROOF_REPLICA_SIGNATURE_MISMATCH = 'Invalid checkpoint proof because checkpoint statement signature mismatch for replica (replica_id, self._id)'
INVALID_CHECKPOINT_PROOF_REPLICA_HASH_MISMATCH = 'Invalid checkpoint proof because hash mismatch for replica (replica_id, self._id)'
INVALID_CHECKPOINT_PROOF_REPLICA_SLOT_MISMATCH = 'Invalid checkpoint proof because slot mismatch for replica (replica_id, self._id)'

# Head messages
RESULT_CACHED = 'Result was cached, returning result from cache to='
RESULT_PENDING = 'Awaiting result shuttle from downstream _replicas'
RESULT_SENT_AFTER_WAIT = 'Result received at head, now forwarding to client='
