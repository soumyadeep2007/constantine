import json

from nacl.exceptions import BadSignatureError


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
        content_json_string = json.dumps(content)
        return private_key.sign(bytes(content_json_string, 'utf-8'))

    @staticmethod
    def is_valid_result(message, replicas, public_keys):
        expected_hash = hash(message["content"]["result"])
        valid_result = True
        replicas_clone = set(replicas)
        for result_statement in message["content"]["result_proof"]:
            valid_result = valid_result and expected_hash == result_statement["hash"]
            public_key = public_keys[result_statement["replica"]["id"]]
            valid_result = valid_result and Commons.is_valid_signature(result_statement, public_key)
            replicas_clone.remove(result_statement["replica"])
        valid_result = valid_result and len(replicas_clone) == 0
        return valid_result
