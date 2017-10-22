# Common messages
INVALID_SIGNATURE = 'A signature mismatch occurred from source:'

# Olympus messages
PARSED_CONFIG = "Parsed config:"
GENERATED_KEYS = 'Generated keys:'
CONFIG_REQUEST_RECEIVED = 'Config request received from client='

# Client messages
REQUESTING_CONFIG = 'Config requested from Olympus by client='
CONFIG_REQUEST_TIMEOUT = 'Config request timed out...retrying...'
CONFIG_FETCHED = 'The _config was fetched from Olympus:'
OPERATION_CREATED = 'The following operation was created:'
REQUEST_MADE = 'A request for an operation was made'
RESULT_SENT = 'A result was sent replica, client='
RESULT_RECEIVED = 'A result was received from replica='
VALID_RESULT_RECEIVED = 'The result received is valid:'
OPERATION_RESULT_PAIR = '>>>>>>>>>>>>The operation result pair is='
REQUEST_TIMEOUT = 'Wait for result timed out for operation='
RETRANSMISSION = 'Retransmitting request to all _replicas for operation='
INVALID_REQUEST_SOURCE = 'Request received from invalid source'


# Replica messages
INVALID_SLOT = 'Shuttle received with invalid request slot'

# Head messages
RESULT_CACHED = 'Result was cached, returning result from cache to='
RESULT_PENDING = 'Awaiting result shuttle from downstream _replicas'
RESULT_SENT_AFTER_WAIT = 'Result received at head, now forwarding to client='

