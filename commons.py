class Commons:
    def is_valid_signature(self, message, publicKey):
        decrypted_content = self.decrypt(message.signedContent, publicKey)
        return decrypted_content == message.content

    def decrypt(self, signed_content, public_key):
        pass
