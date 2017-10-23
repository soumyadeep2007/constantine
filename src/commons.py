import json
from enum import Enum
from nacl.exceptions import BadSignatureError
from nacl.hash import sha256
from nacl.encoding import HexEncoder
from nacl.signing import VerifyKey

class ReplicaState(Enum):
    IMMUTABLE = 0
    ACTIVE = 1


class Commons:
    @staticmethod
    def is_valid_signature(signed_content, public_key):
        public_key_deserialized = VerifyKey(public_key, encoder=HexEncoder)
        try:
            public_key_deserialized.verify(signed_content)
            return True
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
            return Commons.update_running_state(op, key, value)
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