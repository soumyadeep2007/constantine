from enum import Enum
from nacl.exceptions import BadSignatureError
from nacl.hash import sha256
from nacl.encoding import HexEncoder
from nacl.signing import VerifyKey
import log_messages


class ReplicaState(Enum):
    IMMUTABLE = 0
    ACTIVE = 1


class OrderProofValidationState(Enum):
    VALID = 0
    INVALID_ORDER_PROOF_REPLICA_MISSING = 1
    INVALID_ORDER_PROOF_REPLICA_SIGNATURE_MISMATCH = 2
    INVALID_ORDER_PROOF_REPLICA_SLOT_MISMATCH = 3


class Commons:

    @staticmethod
    def is_valid_signature(expected_value, signed_value, public_key):
        public_key_deserialized = VerifyKey(public_key, encoder=HexEncoder)
        try:
            return bytes(str(expected_value), 'utf-8') == public_key_deserialized.verify(signed_value)
        except BadSignatureError:
            return False

    @staticmethod
    def sign(content, private_key):
        return private_key.sign(bytes(str(content), 'utf-8'))

    @staticmethod
    def hash(obj):
        obj_bytes = bytes(str(obj), 'utf-8')
        return sha256(obj_bytes, encoder=HexEncoder)

    @staticmethod
    def perform_operation(command_string, object):
        if command_string is None or not isinstance(command_string, str):
            return 'fail'

        if command_string[0:3] == 'get':
            op = 'get'
            split_op = command_string.split("'")
            if len(split_op) != 3:
                return ''
            key = split_op[1]
            return Commons.update_running_state(op, key, object)
        elif command_string[0:3] == 'put':
            op = 'put'
            split_op = command_string.split("'")
            if len(split_op) != 5:
                return 'fail'
            key = split_op[1]
            value = split_op[3]
            return Commons.update_running_state(op, key, object, value)
        elif command_string[0:6] == 'append':
            op = 'append'
            split_op = command_string.split("'")
            if len(split_op) != 5:
                return 'fail'
            key = split_op[1]
            value = split_op[3]
            return Commons.update_running_state(op, key, object, value)
        elif command_string[0:5] == 'slice':
            op = 'slice'
            split_op = command_string.split("'")
            if len(split_op) != 5:
                return 'fail'
            key = split_op[1]
            value = split_op[3]
            return Commons.update_running_state(op, key, object, value)
        else:
            return 'fail'

    @staticmethod
    def update_running_state(command_type_name, key, object, value=None):
        if command_type_name == 'put':
            object[key] = value
            return 'OK'
        elif command_type_name == 'append':
            if key in object and value is not None:
                object[key] = object[key] + value
                return 'OK'
            else:
                return 'fail'
        elif command_type_name == 'slice':

            if value is None or key not in object:
                return 'fail'
            colon_index = value.find(':')
            if colon_index < 0:
                return 'fail'
            curr_value = object[key]
            start_index = None
            end_index = None
            if colon_index == 0:
                start_index = 0
                if len(value) == 1:
                    end_index = len(curr_value)
            elif colon_index == len(curr_value) - 1:
                end_index = len(curr_value)
            if start_index is None:
                if value[0:colon_index].isdigit():
                    start_index = int(value[0:colon_index])
                else:
                    return 'fail'
            if end_index is None:
                if value[colon_index + 1:].isdigit():
                    end_index = int(value[colon_index + 1:])
                else:
                    return 'fail'

            start_index = start_index if start_index >= 0 else len(curr_value) + start_index
            end_index = end_index if end_index >= 0 else len(curr_value) + end_index

            is_valid_op = key in object
            is_valid_op = is_valid_op and 0 <= start_index and start_index < len(curr_value)
            is_valid_op = is_valid_op and len(curr_value) >= end_index and end_index > start_index
            if is_valid_op:
                object[key] = curr_value[int(start_index):int(end_index)]
                return 'OK'
            else:
                return 'fail'
        elif command_type_name == 'get':
            if key in object:
                return object[key]
            else:
                return ''
        else:
            return 'fail'

    @staticmethod
    def is_valid_order_proof(order_proof, replicas, public_keys, validator_id):
        slot = order_proof['slot']
        operation = order_proof['operation']
        order_stmts = order_proof['order_statements']
        for replica_id in replicas:
            replica_missing = replica_id not in order_stmts
            if replica_missing:
                return False, log_messages.INVALID_ORDER_PROOF_REPLICA_MISSING + " " + replica_id + " " + validator_id
            order_stmt = order_stmts[replica_id]
            if not Commons.is_valid_signature(order_stmt['order_statement'], order_stmt['signed_order_statement'],
                                              public_keys[replica_id]):
                return False, log_messages.INVALID_ORDER_PROOF_REPLICA_SIGNATURE_MISMATCH + " " + replica_id + " " \
                    + validator_id

            order_conflict = slot != order_stmt['order_statement']['slot'] \
                             or operation != order_stmt['order_statement']['operation']
            if order_conflict:
                return False, log_messages.INVALID_ORDER_PROOF_REPLICA_SLOT_MISMATCH + " " + replica_id + " " \
                    + validator_id

        return True, None

    @staticmethod
    def is_valid_result_proof(result_proof, replicas, public_keys, validator_id):
        expected_hash = Commons.hash(result_proof["result"])
        for replica_id in replicas:
            replica_missing = replica_id not in result_proof['result_statements']
            if replica_missing:

                return False, log_messages.INVALID_RESULT_PROOF_REPLICA_MISSING + replica_id + validator_id

            result_stmt_pair = result_proof['result_statements'][replica_id]
            if not Commons.is_valid_signature(result_stmt_pair['result_statement'],
                                              result_stmt_pair['signed_result_statement'],
                                              public_keys[replica_id]):

                return False, log_messages.INVALID_RESULT_PROOF_REPLICA_SIGNATURE_MISMATCH + replica_id + validator_id

            if expected_hash != result_stmt_pair['result_statement']['result_hash']:
                return False, log_messages.INVALID_RESULT_PROOF_REPLICA_HASH_MISMATCH + replica_id + validator_id

        return True, None

    @staticmethod
    def is_valid_checkpoint_proof(checkpoint_proof, replicas, public_keys, validator_id):
        expected_hash = None
        expected_slot = None
        for replica_id in replicas:
            replica_missing = replica_id not in checkpoint_proof['checkpoint_statements']
            if replica_missing:
                return False, log_messages.INVALID_CHECKPOINT_PROOF_REPLICA_MISSING + replica_id + validator_id

            checkpoint_statement_pair = checkpoint_proof['checkpoint_statements'][replica_id]
            if not Commons.is_valid_signature(checkpoint_statement_pair['checkpoint_statement'],
                                              checkpoint_statement_pair['signed_checkpoint_statement'],
                                              public_keys[replica_id]):
                return False, log_messages.INVALID_CHECKPOINT_PROOF_REPLICA_SIGNATURE_MISMATCH + replica_id \
                       + validator_id

            if expected_hash is None:
                expected_hash = checkpoint_statement_pair['checkpoint_statement']['cp_running_state_hash']
            elif expected_hash != checkpoint_statement_pair['checkpoint_statement']['cp_running_state_hash']:
                return False, log_messages.INVALID_CHECKPOINT_PROOF_REPLICA_HASH_MISMATCH + replica_id + validator_id

            if expected_slot is None:
                expected_slot = checkpoint_statement_pair['checkpoint_statement']['slot']
            elif expected_slot != checkpoint_statement_pair['checkpoint_statement']['slot']:
                print(expected_slot)
                print(checkpoint_statement_pair['checkpoint_statement']['slot'])
                return False, log_messages.INVALID_CHECKPOINT_PROOF_REPLICA_SLOT_MISMATCH + replica_id + validator_id

        return True, None

