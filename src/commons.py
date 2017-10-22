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
