import json

from Crypto.Cipher import AES
from hashlib import sha256
from base64 import b64encode, b64decode
from decouple import config


class AESCipher:

    def __init__(self, data, key, iv):
        self.block_size = 32
        self.data = data
        self.key = sha256(key.encode()).digest()[:32]
        self.iv = sha256(iv.encode()).digest()[:16]
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(
            self.block_size - len(s) % self.block_size)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self):
        plain_text = self.pad(self.data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return b64encode(cipher.encrypt(plain_text.encode())).decode()

    def decrypt(self):
        cipher_text = b64decode(self.data.encode())
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.unpad(cipher.decrypt(cipher_text)).decode()


key = config("KEY")
iv = config("IV")


def aes_encrypt(keyword):
    return AESCipher(str(keyword), key, iv).encrypt()


def aes_decrypt(keyword):
    return AESCipher(str(keyword), key, iv).decrypt()


look = {
    "full_name": "Adekunle Abraham",
    "official_email": "loko873n@afexnigeria.com",
    "self_description": "No Fear!",
    "favorite_meal": "Eba and beans"
}
test = aes_encrypt(str(look))
print(test)

# test_2 = aes_decrypt("xLnb+mSMRThG4qVRg4ouPWmlkiSmBW8IaYosE/467q2tKx1d2tsu+PhKtWTnnvW6R7a5XNPPzyn2h/r7A/lgPQ==")
# print(test_2)
