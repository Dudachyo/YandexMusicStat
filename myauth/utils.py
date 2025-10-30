from cryptography.fernet import Fernet
from django.conf import settings

class TokenEncryption:
    def __init__(self):
        self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())


    def encrypt(self, token):
        if not token:
            return None
        return self.cipher.encrypt(token.encode()).decode()

    def decrypt(self, encrypted_token):
        if not encrypted_token:
            return None
        return self.cipher.decrypt(encrypted_token.encode()).decode()

