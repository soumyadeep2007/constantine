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
    def is_valid_result(result_shuttle, replicas, public_keys):
        expected_hash = Commons.hash(message["content"]["result"])
        for replica_id in replicas:
            replica_missing = replica_id not in result_shuttle['content']['result_proof']
            if replica_missing:
                return False

            result_stmt = result_shuttle['content']['result_proof'][replica_id]
            if not Commons.is_valid_signature(result_stmt['signed_content'], public_keys[replica_id]):
                return False

            if expected_hash != result_stmt['content']['result_hash']:
                return False

        return True

    @staticmethod
    def hash(obj):
        obj_bytes = bytes(str(obj), 'utf-8')
        hash_result = {
            'digest': sha256(obj_bytes, encoder=HexEncoder),
            'encoded_message': HexEncoder.encode(obj_bytes)
        }
        return hash_result

    @staticmethod
    def is_valid_order_proof(shuttle, replicas, public_keys):
        slot = shuttle['content']['slot']
        operation = shuttle['content']['operation']
        for replica_id in replicas:
            replica_missing = replica_id not in shuttle['content']['order_proof']
            if replica_missing:
                return False

            order_stmt = shuttle['content']['order_proof'][replica_id]
            if not Commons.is_valid_signature(order_stmt['signed_content'], public_keys[replica_id]):
                return False

            order_conflict = slot != order_stmt['slot'] or operation != order_stmt['operation']
            if order_conflict:
                return False

        return True
