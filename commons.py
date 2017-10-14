import json

from nacl.exceptions import BadSignatureError
from nacl.hash import sha256
from nacl.encoding import HexEncoder


class Commons:
    @staticmethod
    def is_valid_signature(signed_content, public_key):
        try:
            public_key.verify(signed_content)
            return True
        except BadSignatureError:
            return False

    @staticmethod
    def sign(content, private_key):
        return private_key.sign(bytes(str(content), 'utf-8'))

    @staticmethod
    def is_valid_result(message, replicas, public_keys):
        expected_hash = Commons.hash(message["content"]["result"])
        valid_result = True
        replicas_clone = set(replicas)
        for result_statement in message["content"]["result_proof"]:
            valid_result = valid_result and expected_hash == result_statement["hash"]
            public_key = public_keys[result_statement["replica"]["id"]]
            valid_result = valid_result and Commons.is_valid_signature(result_statement, public_key)
            replicas_clone.remove(result_statement["replica"])
        valid_result = valid_result and len(replicas_clone) == 0
        return valid_result

    @staticmethod
    def hash(obj):
        obj_bytes = bytes(str(obj), 'utf-8')
        hash_result = {
            'digest': sha256(obj_bytes, encoder=HexEncoder),
            'encoded_message': HexEncoder.encode(obj_bytes)
        }
        return hash_result
